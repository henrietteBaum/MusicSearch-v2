# ui/central_widget.py
from PySide6.QtWidgets import( 
    QWidget, 
    QHBoxLayout,  
    QTabWidget
)
from PySide6.QtCore import Qt

from ui.tabs.itunes_tab import ItunesTab
from ui.tabs.mb_tab import MbTab
from ui.tabs.literature_tab import LiteratureTab
from core.models import SearchResult

class CentralWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._zoom_level = 100
        self.build_lyout()

    def build_lyout(self):

        # Create main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.all_tabs = QTabWidget()

        self.itunes_tab = ItunesTab()
        self.all_tabs.addTab(self.itunes_tab, "iTunes")

        self.mb_tab = MbTab()
        self.all_tabs.addTab(self.mb_tab, "MusicBrainz")

        self.literature_tab = LiteratureTab()
        self.all_tabs.addTab(self.literature_tab, "Literatur")

        layout.addWidget(self.all_tabs)

    def display_results(self, results: dict[str, SearchResult]):
        self.itunes_tab.display_results(results.get("itunes"))
        self.mb_tab.display_results(results.get("musicbrainz"))

    def clear(self):
         self.itunes_tab.clear()
         self.mb_tab.clear()
         #self.literature_tab.clear()

    # ----- Accessibility -----
    
    def zoom_in(self):
        self.itunes_tab.zoom_in()
        self.mb_tab.zoom_in()
        self.literature_tab.zoom_in()

    def zoom_out(self):
        self.itunes_tab.zoom_out()
        self.mb_tab.zoom_out()
        self.literature_tab.zoom_out()

    def reset_zoom(self):
        self.itunes_tab.reset_zoom()
        self.mb_tab.reset_zoom()
        self.literature_tab.reset_zoom()
    
   



        
