from PySide6.QtWidgets import QMenuBar, QMenu, QApplication
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtCore import Signal

class MenuBar(QMenuBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_menus()

    def _build_menus(self):
        file_menu = self.addMenu("&File")
        # file_menu = QMenu("File", self)
        # self.addAction(file_menu.menuAction())

        #new_action = QAction("New", self)
        #open_action = QAction("Open", self)
        self.save_action = QAction("&Save", self)
        print_action = QAction("&Print", self)
        exit_action = QAction("E&xit", self)

        #file_menu.addAction(new_action)
        #file_menu.addAction(open_action)
        file_menu.addAction(self.save_action)
        #self.save_action.triggered.connect(self.save_current_tab_content())
        file_menu.addAction(print_action)

        file_menu.addSeparator()
        
        file_menu.addAction(exit_action)
        exit_action.triggered.connect(QApplication.instance().quit)


        # View Menu
        view_menu = QMenu("&View", self)
        
        self.zoom_in_action = QAction("Zoom &In", self)
        self.zoom_in_action.setShortcut(QKeySequence.StandardKey.ZoomIn)
        #zoom_in_action.triggered.connect(self.zoom_in_requested)
        
        self.zoom_out_action = QAction("Zoom &Out", self)
        self.zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut)
        #zoom_out_action.triggered.connect(self.zoom_out_requested)

        self.reset_zoom_action = QAction("&Reset Zoom", self)
        self.reset_zoom_action.setShortcut(QKeySequence("Ctrl+0"))
        #reset_zoom_action.triggered.connect(self.reset_zoom_requested)

        view_menu.addAction(self.zoom_in_action)
        view_menu.addAction(self.zoom_out_action)
        view_menu.addAction(self.reset_zoom_action)


        self.addMenu(file_menu)
        self.addMenu(view_menu)

        #self.addAction(view_menu.menuAction())
        # toggle_toolbar_action = QAction("Toggle Toolbar", self, checkable=True)
        # toggle_sidebar_action = QAction("Toggle Sidebar", self, checkable=True)
        # view_menu.addAction(toggle_toolbar_action)
        # view_menu.addAction(toggle_sidebar_action)
        # self.addMenu(view_menu)

        # Help Menu
        help_menu = self.addMenu("&Help")
        help_action = QAction("Documentation", self)
        help_menu.addAction(help_action)
        about_action = QAction("About", self)
        help_menu.addAction(about_action)
        self.addMenu(help_menu)





        

       