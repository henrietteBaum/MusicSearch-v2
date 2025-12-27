# app/ui/main_window.py

from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QLabel

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
)

from app.core.search import search_all


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Music Search v2.1")

        layout = QVBoxLayout()

        # User-Input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search-term..")
        layout.addWidget(self.search_input)

        # Button
        self.search_button = QPushButton("Search")
        layout.addWidget(self.search_button)

        # Output
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)
        
        self.setLayout(layout)

        # Signal
        self.search_button.clicked.connect(self.on_search_clicked)

    def on_search_clicked(self) -> None:
        term = self.search_input.text().strip()

        if not term:
            self.output.setText("Please enter a search-term!")
            return
        
        # Placeholder output:
        self.output.setText(f"Searching for: {term}...")

        try:
            #results = search_all(term)
            tracks, itunes_total, mb_total = search_all(term)
        except Exception as exc:
            self.output.setText(f"Fail on search:\n {exc}")
            return
        
        if not tracks:
            self.output.setText("No matching results.")
            return
        
        header = (
            f"Results found according to API:\n"
            f"iTunes: {itunes_total}\n"
            f"MusicBrainz: {mb_total}\n\n"
        )
        
        lines: list[str] = []

        for track in tracks:
            line = f"{track.artist} - {track.title}"
            if track.album:
                line += f" ({track.album})"
                lines.append(line)

        self.output.setText(header + "\n".join(lines))
        




