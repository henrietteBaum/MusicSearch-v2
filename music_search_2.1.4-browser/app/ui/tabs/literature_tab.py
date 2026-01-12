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

        self.ol_browser = QTextBrowser()
        self.ol_browser.setOpenExternalLinks(True)
        self.ol_browser.setUndoRedoEnabled(False)
        self.ol_browser.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)


        layout.addWidget(self.ol_header)
        layout.addWidget(self.ol_browser)

        # ----- API -----



    # ----- Accessibility -----

    def zoom_in(self):
        self.ol_browser.zoomIn()

    def zoom_out(self):
        self.ol_browser.zoomOut()
    
    def reset_zoom(self):
        self.ol_browser.selectAll()
        self.ol_browser.setFontPointSize(10)

