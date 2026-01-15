# main_window.py
import os

from datetime import datetime

from PySide6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QTabWidget, 
    QFileDialog, 
    QMessageBox,
)
from PySide6.QtCore import Qt, QStandardPaths, QMarginsF
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from PySide6.QtGui import QPageLayout, QPageSize

from ui.menu_bar import MenuBar
from ui.tool_bar import ToolBar
from ui.side_bar import SideBar
from ui.central_widget import CentralWidget

from core.search import search_all
from ui.menu_bar import MenuBar
from ui.tool_bar import ToolBar
from core.models import SearchDomain

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
        # self.tool_bar.music_action.triggered.connect(
        #     self.side_bar.emit_search
        # )

        self.tool_bar.search_domain_group.triggered.connect(self.update_ui_for_domain)
        
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

        # File save from menu Ffile
        self.menu_bar.save_action.triggered.connect(
            self.save_current_tab_content
        )

        # File export to PDF
        self.menu_bar.export_pdf_action.triggered.connect(
            self.export_to_pdf
        )

        # File print from menu File
        self.menu_bar.print_action.triggered.connect(
            self.print_current_tab
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
        print(f"DEBUG: seach started for: {query}")
        try:
            domain = self.tool_bar.get_active_domain()
            print(f"DEBUG: Toolbar sagt Domain ist: {domain} (Typ: {type(domain)})")
            results = search_all(query, limit, domain)
           
            debug_info = [f"{k}: {len(v.tracks)}" for k, v in results.items()]
            print(f"DEBUG: Treffer pro Quelle: {debug_info}")
            #print(f"DEBUG: get results for: {list(results.keys())}")

            self.central_widget.display_results(results)
            self.side_bar.add_to_history(query)

            if domain == SearchDomain.MUSIC:
                self.central_widget.all_tabs.setCurrentIndex(0)
            elif domain == SearchDomain.LITERATURE:
                self.central_widget.all_tabs.setCurrentIndex(2)
        except Exception as e:
            print(f"DEBUG: Error in on_search: {e}")



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
            initial_path.replace(".txt", ".html"),
            "",
            "HTML Files (*.html);;All Files (*)"
            #"Textfiles (*.txt);;All Files (*)"
        )

        if file_path:
            try:
                text_content = current_tab.result_browser.toHtml()
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(text_content)
                self.statusBar().showMessage(f"Saved to {datetime.now().strftime('%H:%M:%S')}", 8000)
            except Exception as e:
                    QMessageBox.critical(self, "Error", f"File could not be saved: {e}")


    # ---- Export to PDF -----
    def export_to_pdf(self):
        tab_container = self.central_widget.all_tabs
        current_tab = tab_container.currentWidget()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

        if current_tab and hasattr(current_tab, "result_browser"):
            active_index = tab_container.currentIndex()
            tab_title = tab_container.tabText(active_index).replace(" ", "_")
            suggested_name = f"{tab_title}_{timestamp}_export.pdf"
            initial_path = os.path.join(self.last_directory, suggested_name)
            
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export to PDF",
                initial_path,
                "PDF Files (*.pdf)"
            )

            if file_path:
                self.last_directory = os.path.dirname(file_path)
                printer = QPrinter(QPrinter.PrinterMode.HighResolution)
                printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
                printer.setOutputFileName(file_path)
                
                size = QPageSize(QPageSize.PageSizeId.A4)
                rientation = QPageLayout.Orientation.Portrait
                #margins = QMarginsF(20, 20, 20, 20)
                
                pdf_layout = QPageLayout(size, QPageLayout.Orientation.Portrait, QMarginsF(20, 20, 20, 20))

                #pdf_layout = QPageLayout(size, orientation, margins)

                printer.setPageLayout(pdf_layout)

            if not current_tab.result_browser.document().isEmpty():
                print("export pdf")
                current_tab.result_browser.print_(printer)
                if os.path.exists(file_path):
                    self.statusBar().showMessage(f"PDF created: {file_path}", 8000)
                    print("pdf exported")
                else:
                    self.statusBar().showMessage("Error: File was not created.", 8000)
            else:
                QMessageBox.warning(self, "Empty", "Nothing to export!")
    

    # ----- Print results from Tab -----
    def print_current_tab(self):
        tab_container = self.central_widget.all_tabs
        current_tab = tab_container.currentWidget()

        if current_tab and hasattr(current_tab, "result_browser"):
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer_dialog = QPrintDialog(printer)

            if printer_dialog.exec() == QFileDialog.Accepted:
                print("printing starts ...")
                current_tab.result_browser.print_(printer)
                print("print successfuly.")
            else:
                print("Print dialog was cancelled.")
