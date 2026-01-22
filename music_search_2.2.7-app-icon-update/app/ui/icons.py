#  app/ui/icons.py

# app/ui/icons.py
import os
import sys
from PySide6.QtGui import QIcon

class IconManager:
    @staticmethod
    def get_icon(theme_name: str, filename: str) -> QIcon:
        """
        Priorisiert lokale Icons aus assets/toolbar_icons für ein konsistentes 
        Erscheinungsbild. Nutzt das System-Theme nur als sekundären Fallback.
        """
        # 1. Pfad robust berechnen
        # Wir gehen davon aus, dass 'app' im Root liegt.
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Wir gehen hoch zum Projekt-Root (von app/ui/ zu root/)
        project_root = os.path.dirname(os.path.dirname(current_dir))
        
        icon_path = os.path.join(project_root, "app", "assets", "toolbar_icons", filename)

        # 2. Lokales Icon laden (Priorität 1)
        if os.path.exists(icon_path):
            return QIcon(icon_path)
        
        # 3. System-Theme (nur wenn lokal nichts gefunden wurde)
        system_icon = QIcon.fromTheme(theme_name)
        if not system_icon.isNull():
            return system_icon

        # 4. Letzter Rettungsanker: Ein leeres Icon oder ein Standard-Fehler-Icon
        print(f"KRITISCH: Icon {filename} weder lokal noch im System gefunden!")
        return QIcon()




# import os
# from PySide6.QtGui import QIcon

# class IconManager:
#     @staticmethod
#     def get_icon(theme_name: str, filename: str) -> QIcon:
#         """
#         Versucht ein Icon aus dem System-Theme zu laden (für KDE/Gnome).
#         Falls das fehlschlägt (Windows/Mac), wird das SVG aus assets/icons geladen.
#         """
#         # 1. Pfad zum assets Ordner berechnen
#         # Wir gehen 3 Ebenen hoch: ui -> app -> root -> assets
#         # (Pass das an, falls deine Struktur anders ist)
#         base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
#         icon_path = os.path.join(base_dir, "assets", "toolbar_icons", filename)

#         # 2. Fallback-Icon erstellen
#         if os.path.exists(icon_path):
#             fallback = QIcon(icon_path)
#         else:
#             print(f"WARNUNG: Icon nicht gefunden: {icon_path}")
#             fallback = QIcon() # Leeres Icon

#         # 3. Die Magie: Theme Icon mit Fallback
#         return QIcon.fromTheme(theme_name, fallback)