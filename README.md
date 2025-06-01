# SteamDown

A Python-based Steam utility application with a modern graphical user interface.

## 🎯 Overview

SteamDown is a desktop application built with Python that provides utilities for Steam users. The application features a clean, modern interface with customizable themes and modular components.

## ✨ Features

- 🎨 **Customizable Themes**: Multiple theme options for personalized experience
- 🖥️ **Modern GUI**: Clean and intuitive user interface
- 📦 **Standalone Executable**: Pre-built executables available for easy installation
- 🔧 **Modular Architecture**: Well-organized codebase with separate components
- 🐍 **Python-based**: Built with Python 3.7.9 for reliability and maintainability

## 🚀 Installation

### Option 1: Download Pre-built Executable
1. Go to the [Releases](../../releases) page
2. Download the latest `SteamDown.exe` file
3. Run the executable directly - no installation required!

### Option 2: Run from Source
1. Clone the repository:
   ```bash
   git clone https://github.com/Avaneesh13/SteamDown.git
   cd SteamDown
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python main.py
   ```

## 🎮 Usage

1. Launch the application by running `SteamDown.exe` or `python main.py`
2. The main window will open with the default theme
3. Navigate through the available features using the interface
4. Customize the appearance by selecting different themes from the options

## 🛠️ Development

### Prerequisites
- Python 3.7.9 or higher
- virtualenv package manager
- Git

### Setting up Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/Avaneesh13/SteamDown.git
   cd SteamDown
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

3. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run in debug mode:
   ```bash
   python main_debug.py
   ```

### Code Structure
- `src/steamdown/`: Main application package
  - `components/`: UI components and windows
  - `themes/`: Theme configurations
  - `utils/`: Utility functions and helpers
  - `assets/`: Static assets (images, icons, etc.)

## 🏗️ Building

The project includes build scripts for creating standalone executables:
## 📋 Requirements

- **Python**: 3.7.9+
- **Operating System**: Windows (primary), macOS and Linux (may require additional setup)
- **Dependencies**: Listed in `requirements.txt`

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit with clear messages: `git commit -m "Add feature description"`
5. Push to your fork: `git push origin feature-name`
6. Submit a pull request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure all builds passes before submitting

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.

## 🐛 Issues and Support

If you encounter any issues or have questions:

1. Create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - System information (OS, Python version)
   - Screenshots if applicable
---

**Note**: This project is not affiliated with Valve Corporation or Steam. Steam is a trademark of Valve Corporation.