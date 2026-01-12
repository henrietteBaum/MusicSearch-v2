# ui/tabs/mb_tab.py

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QTextEdit,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor

from core.formatters.mb_formatter import format_mb_results
from core.models import SearchResult


class MbTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QGridLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        self.mb_output = QTextEdit()
        self.mb_output.setReadOnly(True)

        # layout.addWidget(self.mb_header,0 ,0)
        layout.addWidget(self.mb_output,1 ,0)

    # -------------------------
    # Public API for MainWindow
    # -------------------------

    def display_results(self, result: SearchResult):
        if not result:
            self.clear()
            self.mb_output.setPlaceholderText("No MusicBrainz results.")
            return
        html = format_mb_results(
            tracks=result.tracks,
            total=result.total
        )
        self.mb_output.setHtml(html)

    def clear(self):
        self.mb_output.clear()


   # ----- Accessibility -----

    def zoom_in(self):
        self.mb_output.zoomIn()

    def zoom_out(self):
        self.mb_output.zoomOut()

    # def zoom(self, delta: int):
    #     if delta > 0:
    #         self.mb_output.zoomIn(1)
    #     else:
    #         self.mb_output.zoomOut(1)

    def reset_zoom(self):
        self.mb_output.selectAll()
        self.mb_output.setFontPointSize(10)
        self.mb_output.moveCursor(QTextCursor.Start)

     