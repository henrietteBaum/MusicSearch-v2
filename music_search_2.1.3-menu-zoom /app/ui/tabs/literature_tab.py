# ui/tabs/literatur_tab.py

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
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

        self.ol_output = QTextEdit()
        self.ol_output.setReadOnly(True)

        layout.addWidget(self.ol_header)
        layout.addWidget(self.ol_output)

        # ----- API -----



    # ----- Accessibility -----

    def zoom_in(self):
        self.ol_output.zoomIn()

    def zoom_out(self):
        self.ol_output.zoomOut()
    
    # def zoom(self, delta: int):
    #     if delta > 0:
    #         self.ol_output.zoomIn(1)
    #     else:
    #         self.ol_output.zoomOut(1)

    def reset_zoom(self):
        self.ol_output.selectAll()
        self.ol_output.setFontPointSize(10)
        self.ol_output.moveCursor(QTextCursor.Start)

