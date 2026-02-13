# app/ui/tabs/core_tab.py

from PySide6.QtWidgets import(
    QWidget, 
    QGridLayout, 
    QTextBrowser
)
from PySide6.QtCore import Qt
from core.formatters.core_formatter import format_core_results
from core.models import SearchResult
from ui.ui_styles import get_accent_color

class CoreTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QGridLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        self.result_browser = QTextBrowser()
        self.result_browser.setOpenExternalLinks(True) # Wichtig für Download-Links!
        self.result_browser.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # ----- Accessibility Flags -----
        self.result_browser.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByKeyboard |
            Qt.TextInteractionFlag.TextSelectableByMouse |
            Qt.TextInteractionFlag.LinksAccessibleByKeyboard |
            Qt.TextInteractionFlag.LinksAccessibleByMouse
        )
        
        layout.addWidget(self.result_browser, 0, 0)

    def display_results(self, result: SearchResult):
        if not result or not result.tracks:
            self.result_browser.clear()
            self.result_browser.setPlaceholderText("No scientific results found.")
            return
        
        accent = get_accent_color(self)
        html = format_core_results(
            books=result.tracks,
            total=result.total,
            accent_color=accent
        )
        self.result_browser.setHtml(html)

    def clear(self):
        self.result_browser.clear()