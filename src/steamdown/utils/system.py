import os
import sys
import winreg
import psutil
import subprocess
from threading import Thread
import time
import re

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def get_steam_path():
    """Get Steam installation path from Windows registry"""
    try:
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WOW6432Node\\Valve\\Steam")
        steam_path = winreg.QueryValueEx(hkey, "InstallPath")[0]
        winreg.CloseKey(hkey)
        return steam_path
    except WindowsError:
        try:
            # Try non-WOW6432Node path as fallback
            hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Valve\\Steam")
            steam_path = winreg.QueryValueEx(hkey, "InstallPath")[0]
            winreg.CloseKey(hkey)
            return steam_path
        except WindowsError:
            print("Could not find Steam path in registry")
            return None

def find_steam_processes():
    """Find all Steam-related processes"""
    steam_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            if proc.info['name'] and any(s in proc.info['name'].lower() for s in ['steam', 'steamservice', 'steamwebhelper']):
                steam_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return steam_processes

def get_steam_library_folders():
    """Get all Steam library folders from registry"""
    try:
        steam_path = get_steam_path()
        if not steam_path:
            return []
            
        library_folders = [steam_path]  # Default Steam installation folder
        
        # Read libraryfolders.vdf
        vdf_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")
        if os.path.exists(vdf_path):
            try:
                with open(vdf_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Find all paths in the VDF file
                    paths = re.findall(r'"path"\s+"([^"]+)"', content)
                    library_folders.extend(paths)
            except Exception as e:
                print(f"Error reading libraryfolders.vdf: {e}")
                
        return library_folders
    except Exception as e:
        print(f"Error getting library folders: {e}")
        return []

def get_game_name_from_manifest(app_id, library_folders):
    """Get game name from manifest files in Steam libraries"""
    manifest_name = f"appmanifest_{app_id}.acf"
    
    for library in library_folders:
        manifest_path = os.path.join(library, "steamapps", manifest_name)
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    name_match = re.search(r'"name"\s+"([^"]+)"', content)
                    if name_match:
                        return name_match.group(1)
            except Exception as e:
                print(f"Error reading manifest {manifest_path}: {e}")
    return None

def get_steam_registry_downloads():
    """Get active downloads by monitoring Steam registry keys"""
    try:
        steam_apps_path = r"Software\\Valve\\Steam\\Apps"
        library_folders = get_steam_library_folders()
        
        # Try to open the Steam Apps registry key
        try:
            hkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, steam_apps_path)
        except WindowsError:
            print("Could not find Steam Apps registry key")
            return []
            
        active_downloads = []
        index = 0
        
        # Enumerate all app subkeys
        while True:
            try:
                # Get the name of the subkey (app ID)
                app_id = winreg.EnumKey(hkey, index)
                
                # Open the app's subkey
                app_key_path = f"{steam_apps_path}\\{app_id}"
                app_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, app_key_path)
                
                # Try to get all relevant values at once
                try:
                    values = {}
                    i = 0
                    while True:
                        try:
                            name, data, _ = winreg.EnumValue(app_key, i)
                            values[name] = data
                            i += 1
                        except WindowsError:
                            break
                    
                    # Check if app is being updated or downloaded
                    if values.get('Updating', 0) == 1 or values.get('Downloading', 0) == 1:
                        # Try to get the game name from manifest first
                        game_name = get_game_name_from_manifest(app_id, library_folders)
                        
                        # Fall back to registry name if manifest not found
                        if not game_name:
                            game_name = values.get('Name', f"Game {app_id}")
                            
                        print(f"\nFound active game: {game_name} (ID: {app_id})")
                        print(f"Status - Updating: {values.get('Updating')}, Downloading: {values.get('Downloading')}")
                        
                        # Debug print all values for this app
                        print("Registry values:")
                        for key, value in values.items():
                            print(f"  {key}: {value}")
                        
                        # Get download progress
                        # Try different progress indicators
                        bytes_total = values.get('SizeOnDisk', values.get('BytesToDownload', 0))
                        bytes_downloaded = values.get('BytesDownloaded', 0)
                        download_rate = values.get('DownloadRate', 0)
                        
                        print(f"Download info:")
                        print(f"  Total bytes: {bytes_total}")
                        print(f"  Downloaded: {bytes_downloaded}")
                        print(f"  Rate: {download_rate} bytes/sec")
                        
                        if bytes_total > 0:
                            progress = (bytes_downloaded / bytes_total) * 100
                            print(f"  Progress: {progress:.1f}%")
                        else:
                            progress = 0
                            print("  Progress: Unknown (total size is 0)")
                        
                        active_downloads.append({
                            'app_id': app_id,
                            'name': game_name,
                            'bytes_total': bytes_total,
                            'bytes_downloaded': bytes_downloaded,
                            'download_rate': download_rate
                        })
                        
                except WindowsError as e:
                    if app_id in ['730', '228980', '250820']:  # Common Steam apps
                        print(f"Error reading values for {app_id}: {e}")
                
                winreg.CloseKey(app_key)
                index += 1
                
            except WindowsError:
                break  # No more subkeys
                
        winreg.CloseKey(hkey)
        if active_downloads:
            print(f"\nFound {len(active_downloads)} active downloads")
        return active_downloads
        
    except Exception as e:
        print(f"Error checking Steam registry: {e}")
        return []

def get_steam_status():
    """Get comprehensive Steam status including downloads"""
    try:
        steam_processes = find_steam_processes()
        active_downloads = get_steam_registry_downloads()
        
        return {
            'running': bool(steam_processes),
            'process_count': len(steam_processes),
            'active_downloads': active_downloads,
            'has_downloads': bool(active_downloads)
        }
    except Exception as e:
        print(f"Error getting Steam status: {e}")
        return None

def close_steam_async(callback=None):
    """Close Steam process gracefully in a separate thread"""
    def shutdown_thread():
        try:
            print("Starting Steam shutdown process...")
            result = False
            
            # First check if Steam is running
            steam_processes = find_steam_processes()
            if not steam_processes:
                print("Steam is not running")
                if callback:
                    callback(True)  # Return true since there's nothing to close
                return
            
            print(f"Found {len(steam_processes)} Steam processes")
            
            # Try to close Steam gracefully using the Steam executable
            steam_path = get_steam_path()
            if steam_path:
                print(f"Found Steam path: {steam_path}")
                steam_exe = os.path.join(steam_path, "Steam.exe")
                if os.path.exists(steam_exe):
                    print("Attempting graceful shutdown via Steam.exe -shutdown")
                    try:
                        subprocess.run([steam_exe, "-shutdown"], timeout=5, check=True)
                        print("Shutdown command sent successfully")
                        result = True
                    except subprocess.TimeoutExpired:
                        print("Shutdown command timed out")
                    except subprocess.CalledProcessError as e:
                        print(f"Shutdown command failed: {e}")
            
            if callback:
                callback(result)
                
        except Exception as e:
            print(f"Error during Steam shutdown: {e}")
            if callback:
                callback(False)
    
    # Start the shutdown process in a separate thread
    Thread(target=shutdown_thread, daemon=True).start()
    return True

def system_action(action="shutdown"):
    """Perform system action (shutdown, sleep, hibernate, or log off)"""
    try:
        if action == "shutdown":
            os.system("shutdown /s /t 60 /c \"SteamDown is shutting down the PC. Save your work!\"")
        elif action == "sleep":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif action == "hibernate":
            os.system("shutdown /h")
        elif action == "logoff":
            os.system("shutdown /l")
        return True
    except Exception as e:
        print(f"Error performing system action: {e}")
        return False 