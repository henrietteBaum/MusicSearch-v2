# ui/tabs/literatur_tab.py

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextBrowser
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor

class LiteratureTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        # ----- OpenLibrary -----
        self.ol_header = QLabel("OpenLibrary")
        self.ol_header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.ol_header.setStyleSheet("font-weight:bold;")      

        self.result_browser = QTextBrowser()
        self.result_browser.setOpenExternalLinks(True)
        self.result_browser.setUndoRedoEnabled(False)
        self.result_browser.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # ----- Accessibility -----
        self.result_browser.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByKeyboard |
            Qt.TextInteractionFlag.TextSelectableByMouse |
            Qt.TextInteractionFlag.LinksAccessibleByKeyboard |
            Qt.TextInteractionFlag.LinksAccessibleByMouse
        )

        layout.addWidget(self.ol_header)
        layout.addWidget(self.result_browser)

        # ----- API -----



    # ----- Accessibility -----

    def zoom_in(self):
        self.result_browser.zoomIn()

    def zoom_out(self):
        self.result_browser.zoomOut()
    
    def reset_zoom(self):
        self.result_browser.selectAll()
        self.result_browser.setFontPointSize(10)

