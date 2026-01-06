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

        self.itunes_output = QTextEdit()
        self.itunes_output.setReadOnly(True)

        # ----- MusicBrainz -----
        self.mb_header = QLabel("MusicBrainz")
        self.mb_header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.mb_header.setStyleSheet("font-weight:bold;")

        self.mb_output = QTextEdit()
        self.mb_output.setReadOnly(True)

        layout.addWidget(self.itunes_header)
        layout.addWidget(self.itunes_output)
        layout.addWidget(self.mb_header)
        layout.addWidget(self.mb_output)

    # -------------------
    # Public API for MainWindow
    # -------------------

    def display_results(self, resutls: dict):
        self._display_itunes(resutls.get("itunes"))
        self._display_musicbrainz(resutls.get("musicbrainz"))

    def clear(self):
        self.itunes_output.clear()
        self.mb_output.clear()

    # --------------------
    # Internal helpers
    # --------------------

    def _display_itunes(self, result):
        self.itunes_output.clear()

        if not result:
            self.itunes_output.setPlaceholderText("No itunes results.")
            return
        
        header = (
            f"Results found according to API:\n"
            f"iTunes: {result.total} total, "
            f"showing {len(result.tracks)}\n"
            "-------------------------------\n"
        )
        self.itunes_output.append(header)

        for t in result.tracks:
            line = f"{t.artist} – {t.title}"
            if t.album:
                line += f" ({t.album})"
            self.itunes_output.append(line)

    def _display_musicbrainz(self, result):
        self.mb_output.clear()

        if not result:
            self.mb_output.setPlainText("No MusicBrainz results.")
            return

        header = (
            f"Results found according to API:\n"
            f"MusicBrainz: {result.total} total, "
            f"showing {len(result.tracks)}\n"
            "-------------------------------\n"
        )
        self.mb_output.append(header)

        for t in result.tracks:
            line = f"{t.artist} – {t.title}"
            if t.album:
                line += f" ({t.album})"
            self.mb_output.append(line)
            

