# ui/tabs/itunes.tab.py

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QTextBrowser
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

        self.itunes_browser = QTextBrowser()
        self.itunes_browser.setOpenExternalLinks(True)
        self.itunes_browser.setUndoRedoEnabled(False)
        self.itunes_browser.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        layout.addWidget(self.itunes_browser, 0, 0)

    # -------------------------
    # Public API for MainWindow
    # -------------------------

    def display_results(self, result: SearchResult):
        if not result:
            self.clear()
            self.itunes_browser.setPlaceholderText("No iTunes results")
            return

        html = format_itunes_results(
            tracks=result.tracks,
            total=result.total
        )
        self.itunes_browser.setHtml(html)

    def clear(self):
        self.itunes_browser.clear()

    # ----- Accessibility -----
    def zoom_in(self):
        self.itunes_browser.zoomIn()

    def zoom_out(self):
        self.itunes_browser.zoomOut()

    def reset_zoom(self):
        self.itunes_browser.selectAll()
        self.itunes_browser.setFontPointSize(10)
        self.itunes_browser.moveCursor(QTextCursor.Start)


  