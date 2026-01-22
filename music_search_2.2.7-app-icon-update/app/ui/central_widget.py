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
from core.models import SearchResult
from ui.ui_styles import get_accent_color, get_tab_widget_css 

class CentralWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._zoom_level = 100
        self.build_layout()
        
        # NEU: Styles anwenden
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

  
    def clear(self):
         self.itunes_tab.clear()
         self.mb_tab.clear()
         self.library_tab.clear()

    #----- Styles -----
    def apply_styles(self):
        accent = get_accent_color(self)
        # Style auf das TabWidget anwenden
        self.all_tabs.setStyleSheet(get_tab_widget_css(accent))


# ----- style inside -----
    # def apply_styles(self):
    #     """
    #     Setzt den Style für die Tabs:
    #     - Unterstrich in Akzentfarbe für den aktiven Tab
    #     - Etwas mehr Platz (Padding) für Lesbarkeit
    #     """
    #     # 1. System-Akzentfarbe holen
    #     palette = self.palette()
    #     highlight_color = palette.color(QPalette.Highlight).name()
        
    #     # Optional: Textfarbe des aktiven Tabs auch einfärben?
    #     # Das kann gut aussehen, aber pass auf den Kontrast auf.
    #     # highlight_text = palette.color(QPalette.HighlightedText).name()

    #     self.all_tabs.setStyleSheet(f"""
    #         /* Der Container um die Tabs herum */
    #         QTabWidget::pane {{
    #             border: none; /* Kein Rahmen um den Inhalt, wirkt moderner */
    #             border-top: 1px solid #444; /* Dezente Trennlinie zum Inhalt */
    #             background: transparent;
    #         }}

    #         /* Der Bereich, in dem die Reiter sitzen */
    #         QTabBar {{
    #             background: transparent;
    #         }}

    #         /* Ein einzelner Tab-Reiter */
    #         QTabBar::tab {{
    #             background: transparent;
    #             padding: 10px 20px; /* Großzügiger Klickbereich */
    #             margin-right: 2px;
    #             border-bottom: 3px solid transparent; /* Platzhalter, damit nichts hüpft */
    #             font-size: 11pt; /* Etwas größere Schrift */
    #         }}

    #         /* --- AKTIVER TAB --- */
    #         QTabBar::tab:selected {{
    #             /* Der Unterstrich in deiner Akzentfarbe */
    #             border-bottom: 3px solid {highlight_color};
                
    #             /* Optional: Den Text auch einfärben oder fett machen */
    #             /* color: {highlight_color}; */
    #             font-weight: bold;
                
    #             background-color: rgba(255, 255, 255, 0.05); /* Leichter Hintergrund */
    #         }}

    #         /* --- HOVER (Maus drüber) --- */
    #         QTabBar::tab:hover:!selected {{
    #             background-color: rgba(255, 255, 255, 0.1);
    #             border-bottom: 3px solid rgba(255, 255, 255, 0.3); /* Grauer Unterstrich als Vorschau */
    #         }}
            
    #         /* --- FOCUS (Tastatur Tab-Taste) --- */
    #         QTabBar::tab:focus {{
    #             /* Wichtig für Tastatur-Navigation! */
    #             border: 1px dotted {highlight_color};
    #         }}
    #     """)

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
