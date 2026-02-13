# ui/central_widget.py
from PySide6.QtWidgets import( 
    QWidget, 
    QHBoxLayout,  
    QTabWidget
)
from PySide6.QtGui import QPalette

from ui.tabs.itunes_tab import ItunesTab
from ui.tabs.mb_tab import MbTab
from ui.tabs.library_tab import OpenlibraryTab
from ui.tabs.core_tab import CoreTab
from core.models import SearchResult
from ui.ui_styles import get_accent_color, get_tab_widget_css 

class CentralWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._zoom_level = 100
        self.build_layout()
        
        # Styles anwenden
        self.apply_styles()

    def build_layout(self):

        # Create main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.all_tabs = QTabWidget()
        # WICHTIG für Accessibility: 
        # DocumentMode lässt die Tabs moderner aussehen und entfernt doppelte Rahmen
        self.all_tabs.setDocumentMode(True) 

        self.itunes_tab = ItunesTab()
        self.all_tabs.addTab(self.itunes_tab, "iTunes")

        self.mb_tab = MbTab()
        self.all_tabs.addTab(self.mb_tab, "MusicBrainz")

        self.library_tab = OpenlibraryTab()
        self.all_tabs.addTab(self.library_tab, "OpenLibrary")

        # NEU: CORE Tab hinzufügen
        self.core_tab = CoreTab()
        self.all_tabs.addTab(self.core_tab, "Context (Scientific)")

        layout.addWidget(self.all_tabs)


    def display_results(self, results: dict[str, SearchResult]):
        
        itunes_data = results.get("itunes")
        mb_data = results.get("musicbrainz")
        ol_data = results.get("openlibrary")
        core_data = results.get("core")
        
        if itunes_data:
            self.itunes_tab.display_results(itunes_data)
        
        if mb_data:
            self.mb_tab.display_results(mb_data)
        
        if ol_data:
            self.library_tab.display_results(ol_data)

        # NEU: CORE Daten verteilen
        if core_data:
            self.core_tab.display_results(core_data)

  
    def clear(self):
         self.itunes_tab.clear()
         self.mb_tab.clear()
         self.library_tab.clear()
         self.core_tab.clear()

    #----- Styles for result-tabs -----
    def apply_styles(self):
        accent = get_accent_color(self)
        # Style auf das TabWidget anwenden
        self.all_tabs.setStyleSheet(get_tab_widget_css(accent))

