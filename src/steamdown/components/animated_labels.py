from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Property, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QColor

class AnimatedLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._color = QColor("#ffffff")
        
    def _get_color(self):
        return self._color
        
    def _set_color(self, color):
        self._color = color
        self.setStyleSheet(f"color: {color.name()}")
        
    color = Property(QColor, _get_color, _set_color)

class PulsingLabel(AnimatedLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setup_animation()
        
    def setup_animation(self):
        self.animation = QPropertyAnimation(self, b"color")
        self.animation.setDuration(1500)
        self.animation.setLoopCount(-1)
        
        # Create a sequence of color changes
        self.animation.setStartValue(QColor("#ffffff"))
        self.animation.setEndValue(QColor("#4db8ff"))
        
        # Use easing curve for smooth animation
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()

    def sizeHint(self):
        # Get the font metrics to calculate proper text size
        fm = self.fontMetrics()
        text_width = fm.horizontalAdvance(self.text())
        text_height = fm.height()
        
        # Add extra padding for the larger font
        padding = 40
        return QSize(text_width + padding, text_height + padding)

    def minimumSizeHint(self):
        return self.sizeHint()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Ensure the widget is tall enough for the text
        if event.size().height() < self.sizeHint().height():
            self.setMinimumHeight(self.sizeHint().height()) 