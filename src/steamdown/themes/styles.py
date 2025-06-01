DARK_THEME = """
/* Global styles */
QWidget {
    background-color: #1a1a1a;
    color: #ffffff;
    font-family: 'Segoe UI', Arial, sans-serif;
}

/* Title bar */
#TitleBar {
    background-color: #2d2d2d;
    border-bottom: 1px solid #3d3d3d;
    min-height: 32px;
}

#WindowTitle {
    color: #ffffff;
    font-size: 14px;
    font-weight: bold;
}

#SettingsButton, #BackButton, #CloseButton {
    background: transparent;
    border: none;
    color: #ffffff;
    padding: 5px;
    font-size: 16px;
    min-width: 24px;
    min-height: 24px;
}

#SettingsButton:hover, #BackButton:hover {
    background-color: #3d3d3d;
}

#CloseButton:hover {
    background-color: #c42b1c;
}

/* Main screen */
#MainScreen {
    padding: 20px;
}

#TitleLabel {
    color: #00ff00;
    font-size: 32px;
    font-weight: bold;
    margin: 20px 0;
}

#StatusLabel {
    color: #cccccc;
    font-size: 14px;
    margin: 10px 0;
}

/* Speed indicator */
#SpeedFrame {
    background-color: #2d2d2d;
    border-radius: 4px;
    margin: 10px 0;
    min-height: 8px;
}

#SpeedBar {
    background-color: #00ff00;
    border-radius: 4px;
}

/* Controls */
QComboBox {
    background-color: #2d2d2d;
    border: 1px solid #3d3d3d;
    border-radius: 4px;
    padding: 5px;
    min-height: 25px;
}

QComboBox:hover {
    border-color: #4d4d4d;
}

QComboBox:focus {
    border-color: #00ff00;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: url(down_arrow.png);
}

/* Settings screen */
#SettingsScreen {
    padding: 20px;
}

QSpinBox {
    background-color: #2d2d2d;
    border: 1px solid #3d3d3d;
    border-radius: 4px;
    padding: 5px;
    min-height: 25px;
}

QSpinBox:hover {
    border-color: #4d4d4d;
}

QSpinBox:focus {
    border-color: #00ff00;
}

QCheckBox {
    spacing: 5px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
}

QCheckBox::indicator:unchecked {
    border: 2px solid #3d3d3d;
    background-color: #2d2d2d;
    border-radius: 3px;
}

QCheckBox::indicator:checked {
    border: 2px solid #00ff00;
    background-color: #00ff00;
    border-radius: 3px;
}

/* Form layout */
QFormLayout {
    spacing: 15px;
}

QLabel {
    color: #cccccc;
}

/* Enable button */
#EnableCheck {
    color: #ffffff;
    font-weight: bold;
    font-size: 14px;
}

/* Tooltip */
QToolTip {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #3d3d3d;
    padding: 5px;
}

/* Status messages */
.success {
    color: #00ff00;
}

.warning {
    color: #ffff00;
}

.error {
    color: #ff0000;
}
""" 