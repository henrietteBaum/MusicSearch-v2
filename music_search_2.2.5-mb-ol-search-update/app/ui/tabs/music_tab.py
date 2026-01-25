# ui/tabs/music_tab.py

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
)
from PySide6.QtCore import Qt

class MusicTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        # ----- iTunes -----
        self.itunes_header = QLabel("iTunes")
        self.itunes_header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.itunes_header.setStyleSheet("font-weight:bold;")

        self.itunes_browser = QTextEdit()
        self.itunes_browser.setReadOnly(True)

        # ----- MusicBrainz -----
        self.mb_header = QLabel("MusicBrainz")
        self.mb_header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.mb_header.setStyleSheet("font-weight:bold;")

        self.mb_browser = QTextEdit()
        self.mb_browser.setReadOnly(True)

        layout.addWidget(self.itunes_header)
        layout.addWidget(self.itunes_browser)
        layout.addWidget(self.mb_header)
        layout.addWidget(self.mb_browser)

    # -------------------
    # Public API for MainWindow
    # -------------------

    def display_results(self, results: dict):
        self._display_itunes(results.get("itunes"))
        self._display_musicbrainz(results.get("musicbrainz"))

    def clear(self):
        self.itunes_browser.clear()
        self.mb_browser.clear()

    # --------------------
    # Internal helpers
    # --------------------

    def _display_itunes(self, result):
        self.itunes_browser.clear()

        if not result:
            self.itunes_browser.setPlaceholderText("No itunes results.")
            return
        
        header = (
            f"Results found according to API:\n"
            f"iTunes: {result.total} total, "
            f"showing {len(result.tracks)}\n"
            "-------------------------------\n"
        )
        self.itunes_browser.append(header)

        for t in result.tracks:
            line = f"{t.artist} – {t.title}"
            if t.album:
                line += f" ({t.album})"
            self.itunes_browser.append(line)

    def _display_musicbrainz(self, result):
        self.mb_browser.clear()

        if not result:
            self.mb_browser.setPlainText("No MusicBrainz results.")
            return

        header = (
            f"Results found according to API:\n"
            f"MusicBrainz: {result.total} total, "
            f"showing {len(result.tracks)}\n"
            "-------------------------------\n"
        )
        self.mb_browser.append(header)

        for t in result.tracks:
            line = f"{t.artist} – {t.title}"
            if t.album:
                line += f" ({t.album})"
            self.mb_browser.append(line)
            

