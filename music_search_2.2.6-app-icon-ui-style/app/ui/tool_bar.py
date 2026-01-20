# ui/tool_bar.py
from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QAction, QIcon, QActionGroup, QPalette, QColor
from PySide6 import QtCore
from core.models import SearchDomain
from ui.icons import IconManager
from ui.ui_styles import get_accent_color, get_toolbar_css # <--- Import

class ToolBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__("Search-Tools", parent)
        self.setMovable(False)
        self.setIconSize(QtCore.QSize(28, 28))
        self._build_toolbar()

    def _build_toolbar(self):
        self.search_domain_group = QActionGroup(self)
        self.search_domain_group.setExclusive(True)

        # 1. All Domains
        # Fallback: mt_search.svg
        self.all_action = QAction(
            IconManager.get_icon("edit-find-symbolic", "mt_search.svg"), 
            "All Domains", 
            self
        )
        #self.all_icon = QIcon.fromTheme("edit-find-symbolic")
        #self.all_action = QAction(self.all_icon, "All Domains", self)
        self.all_action.setCheckable(True)
        self.all_action.setChecked(True)
        self.all_action.setToolTip("Search everywhere")

        # 2. Music
        # Fallback: music_note.svg
        self.music_action = QAction(
            IconManager.get_icon("library-music-symbolic", "mt_music_note.svg"),
            "Music", 
            self
        )
        #self.music_icon = QIcon.fromTheme("library-music-symbolic")
        #self.music_action = QAction(self.music_icon, "Music", self)
        self.music_action.setCheckable(True)
        self.music_action.setShortcut("Ctrl+Return")
        self.music_action.setToolTip("Search in iTunes and MusicBrainz")
        self.current_search_domain = SearchDomain.MUSIC

        # 3. Literature
        # Fallback: menu_book.svg
        self.literature_action = QAction(
            IconManager.get_icon("folder-library-symbolic", "mt_library.svg"),
            "Literature", 
            self
        )
        #self.literature_icon = QIcon.fromTheme("folder-library-symbolic")
        #self.literature_action = QAction(self.literature_icon, "Literature", self)
        self.literature_action.setCheckable(True)
        self.literature_action.setShortcut("Ctrl+l")
        self.literature_action.setToolTip("Search literature (OpenLibrary)")

        # 4. Context (Lyrics/Details)
        # Fallback: queue_music.svg oder description.svg
        self.context_action = QAction(
            IconManager.get_icon("view-media-lyrics-symbolic", "mt_music_queue.svg"), 
            "Context", 
            self
        )
        #self.context_icon = QIcon.fromTheme("view-media-lyrics-symbolic")
        #self.context_action = QAction(self.context_icon, "Context", self)
        self.context_action.setCheckable(True)
        self.context_action.setShortcut("Ctrl+y")
        
        # 5. Clear
        # Fallback: delete_sweep.svg
        self.clear_action = QAction(
            IconManager.get_icon("edit-clear-history", "mt_clear_output.svg"), 
            "Clear", 
            self
        )
        #self.clear_icon = QIcon.fromTheme("edit-clear-history")
        #self.clear_action = QAction(self.clear_icon, "Clear", self)
        self.clear_action.setShortcut("Esc")

        self.search_domain_group.addAction(self.all_action)
        self.search_domain_group.addAction(self.music_action)
        self.search_domain_group.addAction(self.literature_action)
        self.search_domain_group.addAction(self.context_action)
  
        self.addAction(self.all_action) 
        self.addAction(self.music_action)
        self.addAction(self.literature_action)
        self.addAction(self.context_action)
        self.addSeparator()
        self.addAction(self.clear_action)

        self.apply_styles()
        #self.apply_kde_style()


    def get_active_domain(self) -> SearchDomain:
        if self.music_action.isChecked():
            return SearchDomain.MUSIC
        if self.literature_action.isChecked():
            return SearchDomain.LITERATURE
        return SearchDomain.ALL

  
    def apply_styles(self):
        # 1. Farbe holen
        accent = get_accent_color(self)
        # 2. CSS holen und setzen
        self.setStyleSheet(get_toolbar_css(accent))


# ----- Alternative KDE-Stil mit Unterstrich innerhalb der Datei -----
    # def apply_kde_style(self):
    #     palette = self.palette()
    #     highlight_color = palette.color(QPalette.Highlight).name()
    
    #     # Wir brauchen eine leicht transparente Version der Highlight-Farbe für den Hintergrund
    #     # oder wir lassen den Hintergrund ganz weg für den puren Unterstrich-Look.
    #     self.setStyleSheet(f"""
    #         QToolBar {{
    #             spacing: 10px;
    #             border: none;
    #             background: transparent;
    #         }}
    #         QToolButton {{
    #             /* Wichtig: Hintergrund muss gesetzt sein, damit Border funktioniert */
    #             background-color: transparent; 
    #             border: none;
    #             border-bottom: 3px solid transparent; /* Platzhalter */
    #             padding-bottom: 4px;
    #             padding-left: 8px;
    #             padding-right: 8px;
    #             margin: 2px;
    #         }}
    #         QToolButton:checked {{
    #             /* Hier wird der Unterstrich in Systemfarbe aktiv */
    #             border-bottom: 3px solid {highlight_color};
    #             background-color: rgba(255, 255, 255, 0.05); /* Ganz dezenter Schimmer */
    #             font-weight: bold;
    #         }}
    #         QToolButton:hover {{
    #             background-color: rgba(255, 255, 255, 0.1);
    #         }}
    #     """)    

# QToolButton { border-bottom: 2px solid {highlight_color}; }
# QToolButton {{
#                padding: 5px;
#                border-radius: 4px;
#            }}