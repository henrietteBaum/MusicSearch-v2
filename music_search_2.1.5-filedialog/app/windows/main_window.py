# main_window.py
import os

from datetime import datetime

from PySide6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QTabWidget, 
    QFileDialog, 
    QMessageBox
)
from PySide6.QtCore import Qt, QStandardPaths


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

        # Hold users directory-preference
        self.last_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)

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

        # Clear browser content
        self.tool_bar.clear_action.triggered.connect(
            self.on_clear
        )

        # File save from menu file
        self.menu_bar.save_action.triggered.connect(
            self.save_current_tab_content
        )

        
        # Zoom from menu view
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

    # ----- File save tab content -----
    def save_current_tab_content(self):
        tab_container = self.central_widget.all_tabs
        current_tab = tab_container.currentWidget()
        #text_content = current_tab.result_browser.toHtml()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    

        if current_tab and hasattr(current_tab, "result_browser"):
            active_index = tab_container.currentIndex()
            tab_title = tab_container.tabText(active_index).replace(" ", "_")
            suggested_name = f"{tab_title}_{timestamp}_export.txt"
            initial_path = os.path.join(self.last_directory, suggested_name)

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Tab-Results",
            initial_path,
            "",
            "Textfiles (*.txt);;All Files (*)"
        )

        if file_path:
            try:
                text_content = current_tab.result_browser.toHtml()
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(text_content)
                self.statusBar().showMessage(f"Saved at {datetime.now().strftime('%H:%M:%S')}", 8000)
            except Exception as e:
                    QMessageBox.critical(self, "Error", f"File could not be saved: {e}")

