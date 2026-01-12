# ui/central_widget.py
from PySide6.QtWidgets import(
    QFrame, 
    QWidget, 
    QHBoxLayout, 
    QVBoxLayout, 
    QTextEdit,
    QTabWidget
)
from PySide6.QtCore import Qt
from ui.tabs.music_tab import MusicTab
from ui.tabs.itunes_tab import ItunesTab
from ui.tabs.mb_tab import MbTab
from ui.tabs.literature_tab import LiteratureTab

class CentralWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.build_lyout()

    def build_lyout(self):

        # Create main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tabs = QTabWidget()

        self.itunes_tab = ItunesTab()
        self.tabs.addTab(self.itunes_tab, "iTunes")

        self.mb_tab = MbTab()
        self.tabs.addTab(self.mb_tab, "MusicBrainz")

        self.literature_tab = LiteratureTab()
        self.tabs.addTab(self.literature_tab, "Literatur")

        layout.addWidget(self.tabs)

    def display_results(self, results):
         self.itunes_tab.display_results(results)
         self.mb_tab.display_results(results)
         #self.literature_tab.display_resutls(results)

    def clear(self):
         self.itunes_tab.clear()
         self.mb_tab.clear()
         #self.literature_tab.clear()
