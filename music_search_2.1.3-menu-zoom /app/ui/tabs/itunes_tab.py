# ui/tabs/itunes.tab.py

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QTextEdit,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor

from core.formatters.itunes_formatter import format_itunes_results
from core.models import SearchResult

class ItunesTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QGridLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        self.itunes_output = QTextEdit()
        self.itunes_output.setReadOnly(True)
        self.itunes_output.setAcceptRichText(True)
        self.itunes_output.setPlaceholderText("No iTunes results.")
        
        layout.addWidget(self.itunes_output, 0, 0)

    # -------------------------
    # Public API for MainWindow
    # -------------------------

    def display_results(self, result: SearchResult):
        if not result:
            self.clear()
            self.itunes_output.setPlaceholderText("No iTunes results")
            return

        html = format_itunes_results(
            tracks=result.tracks,
            total=result.total
        )
        self.itunes_output.setHtml(html)

    def clear(self):
        self.itunes_output.clear()

    # ----- Accessibility -----
    def zoom_in(self):
        self.itunes_output.zoomIn()

    def zoom_out(self):
        self.itunes_output.zoomOut()


    # def zoom(self, delta: int):
    #     if delta > 0:
    #         self.itunes_output.zoomIn(1)
    #     else:
    #         self.itunes_output.zoomOut(1)

    def reset_zoom(self):
        self.itunes_output.selectAll()
        self.itunes_output.setFontPointSize(10)
        self.itunes_output.moveCursor(QTextCursor.Start)


  