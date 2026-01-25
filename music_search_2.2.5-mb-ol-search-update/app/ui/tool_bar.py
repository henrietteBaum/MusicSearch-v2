# ui/tool_bar.py
from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QAction, QIcon, QActionGroup, QPalette, QColor

from core.models import SearchDomain

class ToolBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__("Search-Tools", parent)

        self._build_toolbar()

    def _build_toolbar(self):
        self.search_domain_group = QActionGroup(self)
        self.search_domain_group.setExclusive(True)

        self.all_icon = QIcon.fromTheme("edit-find-symbolic")
        self.all_action = QAction(self.all_icon, "All Domains", self)
        self.all_action.setCheckable(True)
        self.all_action.setChecked(True)
        self.all_action.setToolTip("Search everywhere")

        self.music_icon = QIcon.fromTheme("emblem-music-symbolic")
        self.music_action = QAction(self.music_icon, "Music", self)
        self.music_action.setCheckable(True)
        self.music_action.setShortcut("Ctrl+Return")
        self.music_action.setToolTip("Search in iTunes and MusicBrainz")
        self.current_search_domain = SearchDomain.MUSIC

        self.literature_icon = QIcon.fromTheme("folder-library-symbolic")
        self.literature_action = QAction(self.literature_icon, "Literature", self)
        self.literature_action.setCheckable(True)
        self.literature_action.setShortcut("Ctrl+l")
        self.literature_action.setToolTip("Search literature (OpenLibrary)")

        self.context_icon = QIcon.fromTheme("view-media-lyrics-symbolic")
        self.context_action = QAction(self.context_icon, "Context", self)
        self.context_action.setCheckable(True)
        self.context_action.setShortcut("Ctrl+y")
        
        self.clear_icon = QIcon.fromTheme("edit-clear-history")
        self.clear_action = QAction(self.clear_icon, "Clear", self)
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

        self.apply_kde_style()


    def get_active_domain(self) -> SearchDomain:
        if self.music_action.isChecked():
            return SearchDomain.MUSIC
        if self.literature_action.isChecked():
            return SearchDomain.LITERATURE
        return SearchDomain.ALL

    # def apply_kde_style(self):
    #     # 1. Die Akzentfarbe des Systems auslesen
    #     palette = self.palette()
    #     highlight_color = palette.color(QPalette.Highlight).name()
    #     text_highlight_color = palette.color(QPalette.HighlightedText).name()

    #     # 2. Stylesheet definieren
    #     # Wir stylen den QToolButton, wenn er im Zustand :checked ist
    #     self.setStyleSheet(f"""
    #         QToolBar {{
    #             spacing: 5px; /* Etwas Platz zwischen den Buttons */
    #             border: none;
    #         }}
    #         QToolButton {{
    #             border-bottom: 2px solid {highlight_color};
    #             }}
            
    #         QToolButton:checked {{
    #             background-color: {highlight_color};
    #             color: {text_highlight_color};
    #             border: 1px solid rgba(255, 255, 255, 0.2);
    #         }}
    #         QToolButton:hover:not(:checked) {{
    #             background-color: rgba(255, 255, 255, 0.1);
    #         }}
    #     """)

    def apply_kde_style(self):
        palette = self.palette()
        highlight_color = palette.color(QPalette.Highlight).name()
    
        # Wir brauchen eine leicht transparente Version der Highlight-Farbe für den Hintergrund
        # oder wir lassen den Hintergrund ganz weg für den puren Unterstrich-Look.
        self.setStyleSheet(f"""
            QToolBar {{
                spacing: 10px;
                border: none;
                background: transparent;
            }}
            QToolButton {{
                /* Wichtig: Hintergrund muss gesetzt sein, damit Border funktioniert */
                background-color: transparent; 
                border: none;
                border-bottom: 3px solid transparent; /* Platzhalter */
                padding-bottom: 4px;
                padding-left: 8px;
                padding-right: 8px;
                margin: 2px;
            }}
            QToolButton:checked {{
                /* Hier wird der Unterstrich in Systemfarbe aktiv */
                border-bottom: 3px solid {highlight_color};
                background-color: rgba(255, 255, 255, 0.05); /* Ganz dezenter Schimmer */
                font-weight: bold;
            }}
            QToolButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
        """)    

# QToolButton { border-bottom: 2px solid {highlight_color}; }
# QToolButton {{
#                padding: 5px;
#                border-radius: 4px;
#            }}