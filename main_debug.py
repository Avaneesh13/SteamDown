import sys
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PySide6.QtWidgets import QApplication
from src.steamdown import MainWindow

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s - %(levelname)s - %(message)s')

class CodeChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f"\nCode change detected in {event.src_path}")
            print("Restart the app to apply changes")

def main():
    app = QApplication(sys.argv)
    
    # Set up file watcher
    observer = Observer()
    observer.schedule(CodeChangeHandler(), path='src', recursive=True)
    observer.start()
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    try:
        app.exec()
    finally:
        observer.stop()
        observer.join()

if __name__ == '__main__':
    main() 