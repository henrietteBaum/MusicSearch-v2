# ui/tabs/itunes.tab.py

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QTextBrowser
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor, QPalette
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

        self.result_browser = QTextBrowser()
        self.result_browser.setOpenExternalLinks(True)
        self.result_browser.setUndoRedoEnabled(False)
        self.result_browser.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        layout.addWidget(self.result_browser, 0, 0)

        # ----- Accessibility -----
        self.result_browser.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByKeyboard |
            Qt.TextInteractionFlag.TextSelectableByMouse |
            Qt.TextInteractionFlag.LinksAccessibleByKeyboard |
            Qt.TextInteractionFlag.LinksAccessibleByMouse
        )


    # -------------------------
    # Public API for MainWindow
    # -------------------------

    def display_results(self, result: SearchResult):
        if not result:
            self.clear()
            self.result_browser.setPlaceholderText("No iTunes results")
            return
        
        color = self.palette().color(QPalette.Highlight).name()

        html = format_itunes_results(
            tracks=result.tracks,
            total=result.total,
            accent_color=color
        )
        self.result_browser.setHtml(html)

    def clear(self):
        self.result_browser.clear()

    # ----- Accessibility -----
    def zoom_in(self):
        self.result_browser.zoomIn()

    def zoom_out(self):
        self.result_browser.zoomOut()

    def reset_zoom(self):
        self.result_browser.selectAll()
        self.result_browser.setFontPointSize(10)
        self.result_browser.moveCursor(QTextCursor.Start)


  