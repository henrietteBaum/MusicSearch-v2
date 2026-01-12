# app/ui/main_window.py

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QFrame,
)

from PySide6.QtGui import (
    QAction,
    QIcon
)

from app.ui.search_frame import SearchFrame
from app.ui.output_frame import OutputFrame
from app.core.search import search_all


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Music Search v2.1")
        self.setMinimumSize(800, 600)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Heading
        self.heading = QLabel("Search for music terms.")
        main_layout.addWidget(self.heading)


        self.search_frame = SearchFrame()
        self.output_frame = OutputFrame()

        main_layout.addWidget(self.search_frame)
        main_layout.addWidget(self.output_frame)
        
        # Signal
        self.search_frame.search_requested.connect(self.on_search_clicked)
        self.search_frame.clear_requested.connect(self.clear_requested)
   
    # Event Handlers - Search
    def on_search_clicked(self, term: str, limit: int) -> None:
        self.output_frame.itunes_output.setText(f"Searching for: {term}...")
        self.output_frame.mb_output.setText(f"Searching for: {term}...")

        try:
            results = search_all(term, limit)
        except ConnectionResetError:
            self.output_frame.itunes_output.setText("Connection reset by server. Please try again later.")
            self.output_frame.mb_output.setText("Connection reset by server. Please try again later.")
            return
        except Exception as exc:
            self.output_frame.itunes_output.setText(f"Fail on search:\n {exc}")
            self.output_frame.mb_output.setText(f"Fail on search:\n {exc}")
            return
                                                                                                                                                                                                  
        #results = all_results(term, limit)
        itunes_result = results["itunes"]
        mb_result = results["musicbrainz"]

        itunes_header = (
            f"Results found according to API:\n"
            f"iTunes: {itunes_result.total} total, showing: {len(itunes_result.tracks)}\n"
            "-------------------------------\n"
        )

        mb_header = (
            f"Results found according to API:\n"
            f"MusicBrainz: {mb_result.total} total, shown: {len(mb_result.tracks)}\n"
            "-------------------------------\n"
        )

        self.output_frame.set_itunes_header(itunes_header)
        self.output_frame.show_itunes_results(itunes_result.tracks)
        self.output_frame.set_mb_header(mb_header)
        self.output_frame.show_mb_results(mb_result.tracks)
        
    
    def clear_requested(self) -> None:
        self.output_frame.clear_outputs()
        self.search_frame.clear_inputs()
    

        
        




