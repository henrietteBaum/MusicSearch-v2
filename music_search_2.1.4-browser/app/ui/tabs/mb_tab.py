# ui/tabs/mb_tab.py

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QTextBrowser
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

        self.mb_browser = QTextBrowser()
        self.mb_browser.setOpenExternalLinks(True)
        self.mb_browser.setUndoRedoEnabled(False)
        self.mb_browser.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)


        # layout.addWidget(self.mb_header,0 ,0)
        layout.addWidget(self.mb_browser,1 ,0)

    # -------------------------
    # Public API for MainWindow
    # -------------------------

    def display_results(self, result: SearchResult):
        if not result:
            self.clear()
            self.mb_browser.setPlaceholderText("No MusicBrainz results.")
            return
        html = format_mb_results(
            tracks=result.tracks,
            total=result.total
        )
        self.mb_browser.setHtml(html)

    def clear(self):
        self.mb_browser.clear()


   # ----- Accessibility -----

    def zoom_in(self):
        self.mb_browser.zoomIn()

    def zoom_out(self):
        self.mb_browser.zoomOut()

    def reset_zoom(self):
        self.mb_browser.selectAll()
        self.mb_browser.setFontPointSize(10)

     