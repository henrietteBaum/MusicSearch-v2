# app/main.py

import sys
import os
from PySide6.QtWidgets import QApplication
from windows.main_window import MainWindow
from PySide6.QtGui import QIcon, QGuiApplication
from PySide6 import QtCore, QtWidgets, QtGui

def main() -> None:

    # ----- 1. Wayland-Support für Fedora/Ubuntu (GNOME) -----
    # Das hilft, damit die App nicht über XWayland "verschwommen" gerendert wird
    if sys.platform == "linux":
        os.environ["QT_QPA_PLATFORM"] = "wayland;xcb"

    # 2. Skalierungs-Logik für Qt 6
    # AA_EnableHighDpiScaling wird nicht mehr gebraucht, da in Qt 6 Standard!
    
    # Die Rundungspolicy ist wichtig für 125% oder 150% Skalierung
    # Wichtig: QGuiApplication kommt aus QtGui!
    QtGui.QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)

    # ----- App-Icon -----

    # Icon-Pfad für alle Betriebssysteme, 
    # wir gehen davon aus, dass 'assets' im selben Ordner wie main.py liegt
    base_dir = os.path.dirname(os.path.abspath(__file__))
    #icon_path = os.path.join(base_dir, "assets", "app_icon.svg")
    icon_path = os.path.join(base_dir, "assets", "app_icon_duo.png")


    # 2. Prüfen, ob die Datei da ist (guter Stil)
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        
        # Setzt das Icon für ALLE Fenster der App (auch Popups)
        app.setWindowIcon(app_icon)
    else:
        print(f"Warnung: Icon nicht gefunden unter {icon_path}")


    window = MainWindow()
    window.show()

    # Event‑Loop starten
    sys.exit(app.exec())

if __name__ == "__main__":
    main()