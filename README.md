# SteamDown

A modern, Python-based desktop utility for Steam users.

---

## What is SteamDown?

SteamDown is a utility that monitors Steam download activity. If there is no download activity for a user-defined amount of time, SteamDown will automatically perform your chosen action—such as stopping Steam, shutting down your PC, putting your PC to sleep, and more. This helps automate your system's behavior after downloads finish, saving power and time.

### Key Features
- Monitors Steam download activity and detects inactivity
- Automatically performs actions after downloads finish (shutdown, sleep, stop Steam, and more)
- User-configurable inactivity timer and action selection
- Modern, intuitive GUI
- Easy-to-use standalone executable

**Upcoming:**
- Light & system theme mode
- Bugfixes & performance improvements
- Support for other game launchers (ideas welcome!)

---

### For Developers
- Modular, well-organized codebase
- 100% Python (3.7.9+)

---

## Screenshots

**Main Window**
![Main Window](src\steamdown\assets\screenshots\main_window.png)

**Settings Window**
![Settings Window](src\steamdown\assets\screenshots\settings_window.png)

---

## Getting Started

### 1. Run the App Directly
- Download the latest release from the [Releases](../../releases) page
- Launch `SteamDown.exe` (no installation needed)

### 2. Build from Source
- Clone the repo:
  ```bash
  git clone https://github.com/Avaneesh13/SteamDown.git
  cd SteamDown
  ```
- Create a virtual environment:
  ```bash
  python -m venv venv
  # Windows:
  venv\Scripts\activate
  # macOS/Linux:
  source venv/bin/activate
  ```
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- Run the app:
  ```bash
  python main.py
  ```

### 3. Development & Debug Mode
- To run in debug mode (if supported):
  ```bash
  python main_debug.py
  ```

---

## Usage
- Launch the app and explore the main and settings window
- More features coming soon!

---

## Development

### Prerequisites
- Python 3.7.9 or higher
- Preffered virtual environment manager (venv, virtualenv, etc.)

### Setting Up for Development
1. Clone the repo and set up a virtual environment (see above)
2. Install dev dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run in debug mode:
   ```bash
   python main_debug.py
   ```

### Code Structure
- `src/steamdown/` – Main app package
  - `components/` – UI components
  - `themes/` – Theme configs
  - `utils/` – Utility functions
  - `assets/` – Static assets (images/icons)

---

## Building

To build SteamDown into a standalone executable (Windows):
- Simply run the build script:
  ```bash
  python build.py
  ```
- The output executable will be placed in the `dist/` folder.

## Requirements
- **Python**: 3.7.9+
- **OS**: Windows (primary), macOS/Linux (may need tweaks)
- **Dependencies**: See `requirements.txt`

---

## Contributing

Ideas for new features—especially for supporting other game launchers (e.g., Epic, GOG, Origin, etc.)—are welcome!

### How to Contribute
1. Fork this repo
2. Create a feature branch: `git checkout -b feature-name`
3. Make and test your changes
4. Commit clearly: `git commit -m "Add feature description"`
5. Push: `git push origin feature-name`
6. Open a pull request

### Guidelines
- Follow PEP 8
- Update docs as needed

---

## SteamDown v1.0.0 Release Notes

### 🆕 What's New in v1.0.0
- Initial public release
- Modern GUI
- Standalone Windows executable
- Modular Python codebase

### 🐞 Bugfixes
- Title bar issues fixed
- App icon to be added

### 🔜 Upcoming
- Light/system theme mode
- Support for more launchers (ideas welcome!)

---

## License

MIT License – see [LICENSE](LICENSE) for details.

## Issues & Support
- Open an issue for bugs, suggestions, or questions
- Please include:
  - Description
  - Steps to reproduce
  - OS/Python version
  - Screenshots if possible

---

**Note:** SteamDown is not affiliated with Valve or Steam. Steam is a trademark of Valve Corporation.