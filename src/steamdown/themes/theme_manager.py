from PySide6.QtWidgets import QWidget
import os

from .styles import DARK_THEME
from ..utils.system import resource_path

class ThemeManager:
    def __init__(self):
        self.current_theme = "dark"
        self.themes = {
            "dark": DARK_THEME
        }
        
    def load_theme(self, theme_name: str) -> str:
        """Load a theme by name and return its stylesheet content"""
        if theme_name not in self.themes:
            return ""
            
        return self.themes[theme_name]
    
    def apply_theme(self, widget: QWidget, theme_name: str = "dark") -> None:
        """Apply a theme to a widget and all its children"""
        self.current_theme = theme_name
        stylesheet = self.load_theme(theme_name)
        
        if not stylesheet:
            print("Warning: No stylesheet loaded!")
            return
            
        # Apply new stylesheet
        widget.setStyleSheet(stylesheet)
        
        # Update all child widgets recursively
        def refresh_widget_style(w):
            w.setStyle(w.style())
            w.style().unpolish(w)
            w.style().polish(w)
            w.repaint()
            
            for child in w.findChildren(QWidget):
                refresh_widget_style(child)
        
        refresh_widget_style(widget)
        widget.repaint() 