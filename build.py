import os
import subprocess
import sys
import time
import hashlib
import json
import argparse
import threading
import itertools
from pathlib import Path

# ANSI color codes for Windows
if sys.platform == "win32":
    os.system("color")  # Enable ANSI colors in Windows terminal

# Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Build cache file
CACHE_FILE = ".build_cache"

# Verbosity levels
QUIET = 1      # Only errors and final result
NORMAL = 2     # Basic progress (default)
DETAILED = 3   # More detailed progress
DEBUG = 4      # Full debug output

# Spinner animation
SPINNER_CHARS = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

class Spinner:
    def __init__(self, message="", delay=0.1):
        self.spinner = SPINNER_CHARS
        self.delay = delay
        self.busy = False
        self.spinner_visible = False
        self.message = message
        sys.stdout.write(CYAN)
    
    def write_next(self):
        with self._screen_lock:
            if not self.spinner_visible:
                sys.stdout.write(self.message)
                self.spinner_visible = True
            sys.stdout.write(next(self.spinner_cycle))
            sys.stdout.flush()
            sys.stdout.write('\b')
    
    def remove_spinner(self, cleanup=False):
        with self._screen_lock:
            if self.spinner_visible:
                sys.stdout.write('\b')
                sys.stdout.write(' ')
                sys.stdout.write('\b')
            if cleanup:
                sys.stdout.write('\n')
                sys.stdout.write(RESET)
                sys.stdout.flush()
    
    def spinner_task(self):
        while self.busy:
            self.write_next()
            time.sleep(self.delay)
    
    def __enter__(self):
        self._screen_lock = threading.Lock()
        self.busy = True
        self.spinner_cycle = itertools.cycle(self.spinner)
        self.spinner_thread = threading.Thread(target=self.spinner_task)
        self.spinner_thread.daemon = True
        self.spinner_thread.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.busy = False
        time.sleep(self.delay)
        self.remove_spinner(cleanup=True)

def print_color(text, color, min_verbosity=NORMAL):
    """Print colored text if verbosity level is high enough"""
    if min_verbosity <= verbosity:
        print(f"{color}{text}{RESET}")

def get_file_hash(filepath):
    """Get hash of file contents"""
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def load_cache():
    """Load the build cache"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cache(cache):
    """Save the build cache"""
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)

def get_tracked_files():
    """Get list of files to track for changes"""
    python_files = []
    for root, _, files in os.walk('.'):
        if 'venv' in root or '.git' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith('.py') or file.endswith('.qss'):
                python_files.append(os.path.join(root, file))
    return python_files

def check_for_changes():
    """Check if any tracked files have changed"""
    cache = load_cache()
    tracked_files = get_tracked_files()
    
    # Check if any new files were added
    cached_files = set(cache.get('files', {}))
    current_files = set(tracked_files)
    
    if cached_files != current_files:
        return True
        
    # Check if any existing files were modified
    for file in tracked_files:
        current_hash = get_file_hash(file)
        if current_hash != cache.get('files', {}).get(file):
            return True
            
    return False

def update_cache():
    """Update the build cache with current file hashes"""
    cache = {'files': {}}
    for file in get_tracked_files():
        cache['files'][file] = get_file_hash(file)
    save_cache(cache)

def get_venv_python():
    """Get the Python executable path from virtual environment"""
    if sys.platform == "win32":
        return os.path.join("venv", "Scripts", "python.exe")
    return os.path.join("venv", "bin", "python")

def get_pyside_plugins_path():
    """Get PySide6 plugins path from virtual environment"""
    if sys.platform == "win32":
        return os.path.join("venv", "Lib", "site-packages", "PySide6", "plugins")
    return os.path.join("venv", "lib", "python3.*", "site-packages", "PySide6", "plugins")

def build(force=False):
    """Build the application using PyInstaller"""
    print_color("\n🚀 Building SteamDown...\n", CYAN + BOLD, QUIET)
    
    # Check for changes
    if not force and not check_for_changes():
        print_color("✨ No changes detected since last build", YELLOW, QUIET)
        print_color("📁 Using existing build in 'dist' directory", YELLOW, QUIET)
        print_color("\nUse --force to rebuild anyway", YELLOW, NORMAL)
        return 0
    
    venv_python = get_venv_python()
    pyside_plugins = get_pyside_plugins_path()
    
    # Check Python virtual environment
    if not os.path.exists(venv_python):
        print_color("❌ Error: Python virtual environment not found!", RED, QUIET)
        print_color("Please create a virtual environment first using:", RED, QUIET)
        print_color("python -m venv venv", RED, QUIET)
        print_color("Then install requirements using:", RED, QUIET)
        print_color("pip install -r requirements.txt", RED, QUIET)
        return 1
    
    # Ensure theme files exist
    theme_file = os.path.join("src", "steamdown", "themes", "theme_dark.qss")
    if not os.path.exists(theme_file):
        print_color("❌ Error: Required theme file not found!", RED, QUIET)
        print_color(f"Missing: {theme_file}", RED, QUIET)
        return 1

    print_color("✔ Found theme file", GREEN, NORMAL)
    print_color("✔ Using virtual environment Python", GREEN, NORMAL)
    print_color("\n📦 Starting PyInstaller build...\n", CYAN, NORMAL)

    # PyInstaller command
    cmd = [
        venv_python, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "SteamDown",
        "main.py",
        "--add-data", f"{theme_file}{os.pathsep}steamdown/themes",
        "--add-data", f"{pyside_plugins}{os.pathsep}PySide6/plugins"
    ]

    # Add verbosity flags for PyInstaller
    if verbosity == QUIET:
        cmd.append("--quiet")
    elif verbosity == DETAILED:
        cmd.append("-v")
    elif verbosity == DEBUG:
        cmd.append("-vv")

    try:
        # Use subprocess.PIPE to control output based on verbosity
        stdout = None if verbosity >= DETAILED else subprocess.PIPE
        stderr = None if verbosity >= DETAILED else subprocess.PIPE
        
        with Spinner(" Building... "):
            process = subprocess.run(cmd, check=True, stdout=stdout, stderr=stderr)
        
        print_color("\n✨ Build completed successfully!", GREEN + BOLD, QUIET)
        print_color("📁 Executable can be found in the 'dist' directory", GREEN, QUIET)
        
        # Check if executable was created
        exe_name = "SteamDown.exe" if sys.platform == "win32" else "SteamDown"
        exe_path = os.path.join("dist", exe_name)
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print_color(f"📊 Executable size: {size_mb:.1f}MB", CYAN, QUIET)
            
        # Update cache after successful build
        update_cache()
        return 0
    except subprocess.CalledProcessError as e:
        print_color(f"\n❌ Build failed with error: {e}", RED, QUIET)
        return 1

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Build SteamDown application")
        parser.add_argument("--force", action="store_true", help="Force rebuild even if no changes detected")
        parser.add_argument("-v", "--verbosity", type=int, choices=[1, 2, 3, 4], default=2,
                          help="Verbosity level (1=quiet, 2=normal, 3=detailed, 4=debug)")
        args = parser.parse_args()
        
        # Set global verbosity level
        global verbosity
        verbosity = args.verbosity
        
        sys.exit(build(force=args.force))
    except KeyboardInterrupt:
        print_color("\n\n🛑 Build cancelled by user", RED, QUIET)
        sys.exit(1)
    except Exception as e:
        print_color(f"\n❌ Unexpected error: {e}", RED, QUIET)
        sys.exit(1) 