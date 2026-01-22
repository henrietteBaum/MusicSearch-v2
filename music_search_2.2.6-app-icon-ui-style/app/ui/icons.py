# app/ui/icons.py
import os
from PySide6.QtGui import QIcon

class IconManager:
    @staticmethod
    def get_icon(theme_name: str, filename: str) -> QIcon:
        """
        Versucht ein Icon aus dem System-Theme zu laden (für KDE/Gnome).
        Falls das fehlschlägt (Windows/Mac), wird das SVG aus assets/icons geladen.
        """
        # 1. Pfad zum assets Ordner berechnen
        # Wir gehen 3 Ebenen hoch: ui -> app -> root -> assets
        # (Pass das an, falls deine Struktur anders ist)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        icon_path = os.path.join(base_dir, "app", "assets", "toolbar_icons", filename)

        # 2. Fallback-Icon erstellen
        if os.path.exists(icon_path):
            fallback = QIcon(icon_path)
        else:
            print(f"WARNUNG: Icon nicht gefunden: {icon_path}")
            fallback = QIcon() # Leeres Icon

        # 3. Die Magie: Theme Icon mit Fallback
        return QIcon.fromTheme(theme_name, fallback)