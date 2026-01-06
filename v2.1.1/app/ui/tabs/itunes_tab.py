# ui/tabs/itunes.tab.py

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QTextEdit,
)
from PySide6.QtCore import Qt

class ItunesTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QGridLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

         # ----- iTunes -----
        # self.itunes_header = QLabel("iTunes")
        # self.itunes_header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # self.itunes_header.setStyleSheet("font-weight:bold;")

        self.itunes_output = QTextEdit()
        self.itunes_output.setReadOnly(True)

        #layout.addWidget(self.itunes_header, 0, 0)
        layout.addWidget(self.itunes_output, 1, 0)

    # -------------------------
    # Public API for MainWindow
    # -------------------------

    def display_results(self, resutls: dict):
        self._display_itunes(resutls.get("itunes"))
        #self._display_musicbrainz(resutls.get("musicbrainz"))

    def clear(self):
        self.itunes_output.clear()
        #self.mb_output.clear()

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
