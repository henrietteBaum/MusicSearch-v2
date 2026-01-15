# ui/tool_bar.py
from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QAction, QIcon, QActionGroup

from core.models import SearchDomain

class ToolBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__("Search-Tools", parent)

        self._build_toolbar()

    def _build_toolbar(self):
        self.all_icon = QIcon.fromTheme("edit-find-symbolic")
        self.all_action = QAction(self.all_icon, "All Domains", self)
        self.all_action.setCheckable(True)
        self.all_action.setToolTip("Search everywhere")

        self.music_icon = QIcon.fromTheme("library-music-symbolic")
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

        self.search_domain_group = QActionGroup(self)
        self.search_domain_group.setExclusive(True)


        for action in (
            self.all_action,
            self.music_action,
            self.literature_action,
            self.context_action,
        ):
            self.search_domain_group.addAction(action)
  
        self.addAction(self.all_action) 
        self.addAction(self.music_action)
        self.addAction(self.literature_action)
        self.addAction(self.context_action)
        self.addSeparator()
        self.addAction(self.clear_action)

    def get_active_domain(self) -> SearchDomain:
        if self.music_action.isChecked():
            return SearchDomain.MUSIC
        if self.literature_action.isChecked():
            return SearchDomain.LITERATURE
        return SearchDomain.ALL


  

