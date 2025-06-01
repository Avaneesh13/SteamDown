from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSpinBox, 
                              QFormLayout)
from PySide6.QtCore import Signal, Qt

class SettingsScreen(QWidget):
    # Signals
    settings_changed = Signal(dict)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()
        
        # Inactivity timeout
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 3600)
        self.timeout_spin.setValue(300)
        self.timeout_spin.setButtonSymbols(QSpinBox.UpDownArrows)
        self.timeout_spin.setFocusPolicy(Qt.StrongFocus)
        self.timeout_spin.setAttribute(Qt.WA_MacShowFocusRect, False)  # Remove focus rect on macOS
        self.timeout_spin.valueChanged.connect(self.on_settings_changed)
        form.addRow("Wait time before action (sec):", self.timeout_spin)
        
        layout.addLayout(form)
        self.setLayout(layout)
    
    def on_settings_changed(self, *args):
        """Emit settings changed signal with current values"""
        settings = {
            'inactivity_timeout': self.timeout_spin.value()
        }
        self.settings_changed.emit(settings)
    
    def get_current_settings(self):
        """Get current settings as dictionary"""
        return {
            'inactivity_timeout': self.timeout_spin.value()
        } 