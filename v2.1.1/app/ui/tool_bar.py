# ui/tool_bar.py
from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QAction, QIcon


class ToolBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__("Search-Tools", parent)

        self._build_toolbar()

    def _build_toolbar(self):
        self.search_icon = QIcon.fromTheme("library-music-symbolic")
        self.search_action = QAction(self.search_icon, "Search", self)
        self.search_action.setShortcut("Ctrl+Return")

        self.clear_icon = QIcon.fromTheme("edit-clear-history")
        self.clear_action = QAction(self.clear_icon, "Clear", self)
        self.clear_action.setShortcut("Esc")

        # self.save_icon = QIcon.fromTheme("document-save")
        # self.save_action = QAction(self.save_icon, "Save", self)
        # self.save_action.setShortcut("Ctrl+s")
        # self.addAction(self.save_action)
        
        self.addAction(self.search_action)
        self.addAction(self.clear_action)


