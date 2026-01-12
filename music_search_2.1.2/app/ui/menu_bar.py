from PySide6.QtWidgets import QMenuBar, QMenu, QApplication
from PySide6.QtGui import QAction

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_menus()

    def _build_menus(self):
        # File Menu
        file_menu = self.addMenu("&File")
        # file_menu = QMenu("File", self)
        # self.addAction(file_menu.menuAction())

        new_action = QAction("New", self)
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        exit_action = QAction("Exit", self)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        exit_action.triggered.connect(QApplication.instance().quit)
        self.addMenu(file_menu)

        # View Menu
        view_menu = self.addMenu("&View")
        #view_menu = QMenu("View", self)
        #self.addAction(view_menu.menuAction())
        toggle_toolbar_action = QAction("Toggle Toolbar", self, checkable=True)
        toggle_sidebar_action = QAction("Toggle Sidebar", self, checkable=True)
        view_menu.addAction(toggle_toolbar_action)
        view_menu.addAction(toggle_sidebar_action)
        self.addMenu(view_menu)

        # Help Menu
        help_menu = self.addMenu("&Help")
        #help_menu = QMenu("Help", self)
        #self.addAction(help_menu.menuAction())
        help_action = QAction("Documentation", self)
        help_menu.addAction(help_action)
        about_action = QAction("About", self)
        help_menu.addAction(about_action)
        self.addMenu(help_menu)

    # def _close_parent(self):
    #     parent = self.parent()
    #     if parent is not None:
    #         parent.close()



        

       