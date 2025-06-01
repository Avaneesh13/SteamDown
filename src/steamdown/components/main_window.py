from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                              QHBoxLayout, QStackedWidget, QFrame, QComboBox, QCheckBox)
from PySide6.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QIcon, QColor
from collections import deque
import os
import time

from .animated_labels import PulsingLabel, AnimatedLabel
from .settings import SettingsScreen
from ..utils.system import (close_steam_async, get_steam_status, system_action, resource_path)
from ..themes.theme_manager import ThemeManager

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(400, 500)
        self.dragging = False
        self.drag_position = QPoint()
        
        # Initialize settings
        self.inactivity_timeout = 300  # seconds
        self.steam_closed = False
        self.enabled = False
        self.below_threshold_start = None
        self.shutdown_in_progress = False
        self.system_action = 'shutdown'
        
        # Initialize theme manager
        self.theme_manager = ThemeManager()
        
        # Setup UI
        self.setup_ui()
        
        # Apply initial theme
        self.theme_manager.apply_theme(self, "dark")
        
        # Start monitoring
        self.timer = QTimer()
        self.timer.timeout.connect(self.monitor_downloads)
        self.timer.start(1000)
    
    def setup_ui(self):
        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        
        # Add title bar
        self.setup_title_bar()
        
        # Create stacked widget
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("MainContent")
        
        # Create and add main screen
        self.main_screen = self.create_main_screen()
        self.stacked_widget.addWidget(self.main_screen)
        
        # Create and add settings screen
        self.settings_screen = SettingsScreen()
        self.settings_screen.settings_changed.connect(self.on_settings_changed)
        self.stacked_widget.addWidget(self.settings_screen)
        
        main_layout.addWidget(self.stacked_widget)
    
    def setup_title_bar(self):
        title_bar = QWidget()
        title_bar.setObjectName("TitleBar")
        title_bar_layout = QHBoxLayout()
        title_bar_layout.setContentsMargins(10, 5, 10, 5)
        title_bar_layout.setSpacing(0)
        
        # Window title with Steam icon
        title_layout = QHBoxLayout()
        title_layout.setSpacing(10)
        
        title_icon = QLabel()
        title_icon.setPixmap(QIcon(resource_path("assets/steam_icon.png")).pixmap(16, 16))
        title_layout.addWidget(title_icon)
        
        title_label = QLabel("SteamDown")
        title_label.setObjectName("WindowTitle")
        title_layout.addWidget(title_label)
        
        # Settings/Back button
        self.settings_button = QPushButton("⚙")
        self.settings_button.setObjectName("SettingsButton")
        self.settings_button.clicked.connect(self.switch_to_settings)
        self.settings_button.setCursor(Qt.PointingHandCursor)
        self.settings_button.setToolTip("Settings")
        
        self.back_button = QPushButton("←")
        self.back_button.setObjectName("SettingsButton")  # Use same style as settings button
        self.back_button.clicked.connect(self.switch_to_main)
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.setToolTip("Back to main screen")
        self.back_button.hide()
        
        # Close button
        close_button = QPushButton("✕")
        close_button.setObjectName("CloseButton")
        close_button.clicked.connect(self.close)
        close_button.setCursor(Qt.PointingHandCursor)
        close_button.setToolTip("Close")
        
        title_bar_layout.addLayout(title_layout)
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(self.settings_button)
        title_bar_layout.addWidget(self.back_button)
        title_bar_layout.addWidget(close_button)
        
        title_bar.setLayout(title_bar_layout)
        self.layout().addWidget(title_bar)
    
    def create_main_screen(self):
        widget = QWidget()
        widget.setObjectName("MainScreen")
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 20, 30, 30)
        
        # Status section
        status_widget = QWidget()
        status_layout = QVBoxLayout()
        status_layout.setSpacing(10)
        
        # Animated title
        self.title = PulsingLabel("STEAMDOWN")
        self.title.setObjectName("TitleLabel")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFixedHeight(60)
        status_layout.addWidget(self.title)
        
        # Status label
        self.status = AnimatedLabel("Monitoring Steam downloads...")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setObjectName("StatusLabel")
        status_layout.addWidget(self.status)
        
        # Active downloads section
        self.downloads_label = QLabel("No active downloads")
        self.downloads_label.setAlignment(Qt.AlignCenter)
        self.downloads_label.setObjectName("DownloadsLabel")
        self.downloads_label.setWordWrap(True)
        status_layout.addWidget(self.downloads_label)
        
        status_widget.setLayout(status_layout)
        layout.addWidget(status_widget)
        
        # Controls section
        controls_widget = QWidget()
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(15)
        
        # Action selection
        self.action_combo = QComboBox()
        self.action_combo.setObjectName("ActionCombo")
        self.action_combo.addItems(["Gracefully stop Steam", "Shutdown PC", "Sleep PC", "Hibernate PC", "Log off"])
        self.action_combo.setCurrentText("Gracefully stop Steam")
        controls_layout.addWidget(self.action_combo)
        
        # Enable checkbox
        enable_layout = QHBoxLayout()
        enable_layout.setAlignment(Qt.AlignCenter)
        
        self.enable_check = QCheckBox("Enable SteamDown")
        self.enable_check.setObjectName("EnableCheck")
        self.enable_check.stateChanged.connect(self.on_toggle_changed)
        enable_layout.addWidget(self.enable_check)
        
        controls_layout.addLayout(enable_layout)
        
        controls_widget.setLayout(controls_layout)
        layout.addWidget(controls_widget)
        
        # Add stretches for better spacing
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.y() <= 40:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()
    
    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
    
    def switch_to_settings(self):
        """Switch to settings screen"""
        self.settings_button.hide()
        self.back_button.show()
        self.stacked_widget.setCurrentWidget(self.settings_screen)
    
    def switch_to_main(self):
        """Switch back to main screen"""
        self.back_button.hide()
        self.settings_button.show()
        self.stacked_widget.setCurrentWidget(self.main_screen)
    
    def on_settings_changed(self, settings):
        """Handle settings changes"""
        try:
            # Reset monitoring state when settings change
            self.below_threshold_start = None
            self.steam_closed = False
            
            # Update settings with validation
            new_timeout = settings.get('inactivity_timeout', 300)
            
            # Ensure values are within reasonable ranges
            if new_timeout <= 0:
                new_timeout = 300
                
            self.inactivity_timeout = new_timeout
            
            print(f"Settings updated - Timeout: {new_timeout}s")
            
        except Exception as e:
            print(f"Error updating settings: {e}")
            # Revert to default values if there's an error
            self.inactivity_timeout = 300
    
    def on_toggle_changed(self, state):
        """Handle enable/disable toggle"""
        self.enabled = bool(state)
        if not self.enabled:
            self.steam_closed = False
            self.below_threshold_start = None
            self.status.setText("Automatic actions disabled")
    
    def monitor_downloads(self):
        """Monitor Steam downloads and take action if needed"""
        try:
            if self.steam_closed:
                return
                
            # Get Steam status
            steam_status = get_steam_status()
            if not steam_status:
                return
                
            # Check if there are any active Steam downloads
            active_downloads = steam_status['active_downloads']
            
            # Update active downloads display
            if active_downloads:
                # Format download information with progress
                download_lines = []
                has_active_download = False
                for download in active_downloads:
                    try:
                        # Create simple status line
                        status_line = f"• {download['name']}"
                        download_lines.append(status_line)
                        
                        # Download is considered active if it's in the active_downloads list
                        # since get_steam_registry_downloads() already checks Updating/Downloading state
                        has_active_download = True
                    except KeyError:
                        # If we can't get basic info, show basic info
                        download_lines.append(f"• {download['name']} (Downloading...)")
                        has_active_download = True
                
                downloads_text = "Active downloads:\n" + "\n".join(download_lines)
                self.downloads_label.setText(downloads_text)
                
                # Only start timing if there's NO active download
                if not has_active_download and self.enabled:
                    if self.below_threshold_start is None:
                        self.below_threshold_start = time.time()
                        print("No active downloads detected, starting timer")
                    
                    # Check if we've waited long enough
                    time_below = time.time() - self.below_threshold_start
                    if time_below >= self.inactivity_timeout:
                        print(f"No active downloads for {time_below:.1f} seconds, performing action")
                        self.perform_action()
                    else:
                        self.status.setText(f"No active downloads. Action in: {int(self.inactivity_timeout - time_below)} seconds")
                else:
                    # Reset timer if there are active downloads
                    self.below_threshold_start = None
                    if self.enabled:
                        self.status.setText("Active download detected, waiting...")
                    else:
                        self.status.setText("Automatic actions disabled")
            else:
                # No downloads at all, start timer
                if self.enabled:
                    if self.below_threshold_start is None:
                        self.below_threshold_start = time.time()
                        print("No downloads detected, starting timer")
                    
                    time_below = time.time() - self.below_threshold_start
                    if time_below >= self.inactivity_timeout:
                        print(f"No downloads for {time_below:.1f} seconds, performing action")
                        self.perform_action()
                    else:
                        self.status.setText(f"No downloads. Action in: {int(self.inactivity_timeout - time_below)} seconds")
                else:
                    self.status.setText("Automatic actions disabled")
                self.downloads_label.setText("No active downloads")
            
        except Exception as e:
            print(f"Error in download monitoring: {e}")
            self.below_threshold_start = None
    
    def on_steam_shutdown_complete(self, success):
        """Handle the completion of Steam shutdown"""
        if success:
            self.steam_closed = True
            self.status.setText("Steam has been closed due to low download speed")
        else:
            self.status.setText("Failed to close Steam completely. Try closing it manually.")
        self.shutdown_in_progress = False
    
    def perform_action(self):
        """Perform selected action when conditions are met"""
        if self.steam_closed or self.shutdown_in_progress:
            return
            
        self.shutdown_in_progress = True
        selected_action = self.action_combo.currentText()
        
        if selected_action == "Gracefully stop Steam":
            self.status.setText("Attempting to close Steam...")
            close_steam_async(callback=self.on_steam_shutdown_complete)
        else:
            # Map UI text to system action
            action_map = {
                "Shutdown PC": "shutdown",
                "Sleep PC": "sleep",
                "Hibernate PC": "hibernate",
                "Log off": "logoff"
            }
            action = action_map.get(selected_action)
            if action:
                self.status.setText(f"Performing {selected_action}...")
                if system_action(action):
                    if action == "shutdown":
                        self.status.setText("PC will shutdown in 60 seconds...")
                    else:
                        self.status.setText(f"Performing {selected_action}...")
                else:
                    self.status.setText(f"Failed to perform {selected_action}")
            self.shutdown_in_progress = False 