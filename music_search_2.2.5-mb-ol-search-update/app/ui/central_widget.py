# ui/central_widget.py
from PySide6.QtWidgets import( 
    QWidget, 
    QHBoxLayout,  
    QTabWidget
)
from PySide6.QtCore import Qt

from ui.tabs.itunes_tab import ItunesTab
from ui.tabs.mb_tab import MbTab
from ui.tabs.library_tab import OpenlibraryTab
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

        self.library_tab = OpenlibraryTab()
        self.all_tabs.addTab(self.library_tab, "OpenLibrary")

        layout.addWidget(self.all_tabs)


    def display_results(self, results: dict[str, SearchResult]):
        
        itunes_data = results.get("itunes")
        mb_data = results.get("musicbrainz")
        ol_data = results.get("openlibrary")
        
        if itunes_data:
            self.itunes_tab.display_results(itunes_data)
        
        if mb_data:
            self.mb_tab.display_results(mb_data)
        
        if ol_data:
            self.library_tab.display_results(ol_data)

    # def display_library_results(self, results: dict[str, SearchResult]):
    #     self.library_tab.display_results(results.get("openlibrary"))


    def clear(self):
         self.itunes_tab.clear()
         self.mb_tab.clear()
         self.library_tab.clear()

    # ----- Accessibility -----
    
    def zoom_in(self):
        self.itunes_tab.zoom_in()
        self.mb_tab.zoom_in()
        self.library_tab.zoom_in()

    def zoom_out(self):
        self.itunes_tab.zoom_out()
        self.mb_tab.zoom_out()
        self.library_tab.zoom_out()

    def reset_zoom(self):
        self.itunes_tab.reset_zoom()
        self.mb_tab.reset_zoom()
        self.library_tab.reset_zoom()
