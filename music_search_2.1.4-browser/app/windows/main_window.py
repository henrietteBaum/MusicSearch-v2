# main_window.py

from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtCore import Qt


from ui.menu_bar import MenuBar
from ui.tool_bar import ToolBar
from ui.side_bar import SideBar
from ui.central_widget import CentralWidget

from core.search import search_all
from ui.menu_bar import MenuBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MusicSearch")
        self.resize(800, 600)


        # Set up Menu Bar
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        # short way:
        # self.setMenuBar(MenuBar(self))

        # Set up Tool Bar
        self.tool_bar = ToolBar(self)
        self.addToolBar(self.tool_bar)
        
        # Set up Side Bar
        self.side_bar = SideBar(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.side_bar)

        # Set up Central Widget
        self.central_widget = CentralWidget(self)
        self.setCentralWidget(self.central_widget)

        self._connect_signals()
    
    def _connect_signals(self):
        # toolbar-butten starts the method inside sidebar: 
        self.tool_bar.search_action.triggered.connect(
            self.side_bar.emit_search
        )
        
        # the custom-signal from sidebar calls the external logic from module tool_bar_actions
        # string from emit() will be sent automaticaly to on_search
        # self.sidebar.searchRequested.connect(on_search)

        self.side_bar.searchRequestet.connect(
            self.on_search
        )

        self.tool_bar.clear_action.triggered.connect(
            self.on_clear
        )
        
        self.menu_bar.zoom_in_action.triggered.connect(
            self.central_widget.zoom_in
        )
        self.menu_bar.zoom_out_action.triggered.connect(
            self.central_widget.zoom_out
        )
        self.menu_bar.reset_zoom_action.triggered.connect(
            self.central_widget.reset_zoom
        )
 
    def on_search(self, query: str, limit: int):
        results = search_all(query, limit)
        self.central_widget.display_results(results)
    
        self.side_bar.add_to_history(query)
    
    def on_clear(self):
        self.central_widget.clear()

    # ----- Accessibility -----
    def zoom_in(self):
        self.central_widget.zoom(1)
    
    def zoom_out(self):
        self.central_widget.zoom(-1)

    def reset_zoom(self):
        self.central_widget.reset_zoom()
    



