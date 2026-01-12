# ui/tabs/mb_tab.py

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QTextEdit,
)
from PySide6.QtCore import Qt
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

    # def _display_musicbrainz(self, result):
    #     self.mb_output.clear()

    #     if not result:
    #         self.mb_output.setPlainText("No MusicBrainz results.")
    #         return

    #     header = (
    #         f"Results found according to API:\n"
    #         f"MusicBrainz: {result.total} total, "
    #         f"showing {len(result.tracks)}\n"
    #         "-------------------------------\n"
    #     )
    #     self.mb_output.append(header)

    #     for t in result.tracks:
    #         line = f"{t.artist} – {t.title}"
    #         if t.album:
    #             line += f" ({t.album})"
    #         self.mb_output.append(line)        