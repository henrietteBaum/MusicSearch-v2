# main_window.py

from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtCore import Qt


from ui.menu_bar import MenuBar
from ui.tool_bar import ToolBar
from ui.side_bar import SideBar
from ui.central_widget import CentralWidget
from core.search import search_all



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MusicSearch")
        self.resize(800, 600)

        # self.tray_icon = QSystemTrayIcon(self)
        # self.tray_icon.setIcon(QIcon.fromTheme("library-music-symbolic"))
        # self.tray_menu = QMenu(self)
        # self.tray_icon.show()

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
  
    def on_search(self, query: str, limit: int):
        results = search_all(query, limit)
        self.central_widget.display_results(results)

        # if not query:
        #     return
        # # dummy-result
        # results = {
        #     "query": query,
        #     "limit": limit
        # }

        # limit = self.side_bar.limit_input.value()
        # results = search_all(term=query, limit=limit)
    
        self.central_widget.display_results(results)

        self.side_bar.add_to_history(query)
    
    def on_clear(self):
        #self.side_bar.clear_input()
        #self.side_bar.search_input.setCurrentText("")
        self.central_widget.clear()
    



