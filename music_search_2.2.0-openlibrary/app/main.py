# app/main.py

import sys
#from pathlib import Path
from PySide6.QtWidgets import QApplication
from windows.main_window import MainWindow

def main() -> None: 
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    # Event‑Loop starten
    sys.exit(app.exec())

if __name__ == "__main__":
    main()