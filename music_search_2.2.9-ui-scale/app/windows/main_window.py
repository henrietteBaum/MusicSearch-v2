# main_window.py
import os

from datetime import datetime

from PySide6.QtWidgets import (
    QMainWindow, 
    QFileDialog, 
    QMessageBox,
)
from PySide6.QtCore import Qt, QStandardPaths, QMarginsF, QSize
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from PySide6.QtGui import QPageLayout, QPageSize, QGuiApplication, Qt

from ui.menu_bar import MenuBar
from ui.tool_bar import ToolBar
from ui.side_bar import SideBar
from ui.central_widget import CentralWidget
from windows.help_window import HelpWindow   

from core.models import SearchDomain
from core.search_worker import SearchWorker
from core.ui_zoom import UIZoomFilter 

from ui.ui_styles import (
    get_accent_color, get_menubar_css, get_toolbar_css,
    get_search_button_css, get_tab_widget_css
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MusicSearch")
        self.resize(800, 600)
        self.help_window = None

        self.detect_dark_mode()

        # UI Zoom initialisieren
        self.ui_zoom = UIZoomFilter(self)
        self.ui_zoom.zoomChanged.connect(self.update_scaling)

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
        # Search request from Side Bar
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

        # Help -> Documentation
        self.menu_bar.help_action.triggered.connect(
            self.show_documentation
        )
        # Help -> About
        self.menu_bar.about_action.triggered.connect(
            self.show_about_dialog
        )

        # Die Menü-Aktionen (und damit auch Strg++ / Strg+-) steuern jetzt den UI-Zoom
        self.menu_bar.zoom_in_action.triggered.connect(self.ui_zoom.zoom_in)
        self.menu_bar.zoom_out_action.triggered.connect(self.ui_zoom.zoom_out)
        self.menu_bar.reset_zoom_action.triggered.connect(self.ui_zoom.reset_zoom)

        # Optional: Feedback in Statusbar
        self.ui_zoom.zoomChanged.connect(
            lambda val: self.statusBar().showMessage(f"UI Zoom: {val}", 8000)
        )

    def update_scaling(self, zoom_percent_str):
        # 1. Aktuellen Zoom-Faktor holen (float, z.B. 1.2)
        scale = self.ui_zoom.current_zoom
        
        # 2. Aktuelle Akzentfarbe holen
        accent = get_accent_color(self)
        
        # Feedback in Statusbar
        self.statusBar().showMessage(f"UI Zoom: {zoom_percent_str}", 8000)

        # --- 1. TOOLBAR (Braucht accent UND scale) ---
        new_icon_size = int(32 * scale)
        self.tool_bar.setIconSize(QSize(new_icon_size, new_icon_size))
        self.tool_bar.setStyleSheet(get_toolbar_css(accent, scale))

        # --- 2. MENUBAR (Braucht NUR scale) ---
        # HIER WAR DER FEHLER: Wir übergeben nur 'scale', kein 'accent'
        self.menu_bar.setStyleSheet(get_menubar_css(accent, scale))

        # --- 3. SIDEBAR BUTTON (Braucht accent UND scale) ---
        self.side_bar.search_button.setStyleSheet(get_search_button_css(accent, scale))

        # --- 4. TABS (Braucht accent UND scale) ---
        self.central_widget.all_tabs.setStyleSheet(get_tab_widget_css(accent, scale))
        




        # Zoom from menu view for search-results
        # self.menu_bar.zoom_in_action.triggered.connect(
        #     self.central_widget.zoom_in
        # )
        # self.menu_bar.zoom_out_action.triggered.connect(
        #     self.central_widget.zoom_out
        # )
        # self.menu_bar.reset_zoom_action.triggered.connect(
        #     self.central_widget.reset_zoom
        # )
  
    def on_search(self, query: str, limit: int, mode: str):
        print(f"DEBUG: seach started for: {query} in mode: {mode} with limit: {limit}")

        try:
            domain = self.tool_bar.get_active_domain()
            print(f"DEBUG: Toolbar sagt Domain ist: {domain} (Typ: {type(domain)})")
            #results = search_all(query, limit, domain)
           
            #debug_info = [f"{k}: {len(v.tracks)}" for k, v in results.items()]
            #print(f"DEBUG: Treffer pro Quelle: {debug_info}")

            self.statusBar().showMessage(f"Searching for '{query}' ({mode})...")
            self.side_bar.search_button.setEnabled(False)

            # Domain holen (Musik vs Literatur vs Alle)
            domain = self.tool_bar.get_active_domain()

            # Suchbegriff zur History hinzufügen
            self.side_bar.add_to_history(query)

            # Starte den Such-Worker-Thread        
            self.worker = SearchWorker(query, limit, domain, mode)
            self.worker.results_ready.connect(self.on_search_finished)
            self.worker.start()


        except Exception as e:
            print(f"DEBUG: Error in on_search: {e}")


    def apply_tab_focus(self):
        """Wechselt den aktiven Tab basierend auf der gewählten Such-Domain."""
        domain = self.tool_bar.get_active_domain()
    
        if domain == SearchDomain.MUSIC:
        # Index 0 ist iTunes (oder nach Belieben 1 für MusicBrainz)
            self.central_widget.all_tabs.setCurrentIndex(0)
    
        elif domain == SearchDomain.LITERATURE:
        # Index 2 ist OpenLibrary
            self.central_widget.all_tabs.setCurrentIndex(2)
    
        # Bei SearchDomain.ALL lassen wir den Tab meist so, wie er ist, 
        # oder springen zum ersten (iTunes).

    def on_search_finished(self, results: dict):
        # 1. Ergebnisse an die Tabs verteilen
        self.central_widget.display_results(results)
        # 2. UI wieder aktiv schalten
        self.side_bar.search_button.setEnabled(True)
        self.statusBar().showMessage("Ready", 8000)
        # 3. Den automatischen Tab-Wechsel (optional)
        self.apply_tab_focus()    
        

    def on_clear(self):
        self.central_widget.clear()

    # ---- Help - Documentation Window -----
    def show_documentation(self):
        if self.help_window is None:
            #self.help_window = HelpWindow(self)
            color = self.palette().color(self.palette().ColorRole.Highlight).name()
            self.help_window = HelpWindow(color, parent=None)
        self.help_window.show()
        self.help_window.raise_()
        self.help_window.activateWindow()

    # ----- Help - About -----
    def show_about_dialog(self):
        QMessageBox.about(
            self,
            "About this App",
            """
            <h3>Media Search App</h3>
            <p>Version 2</p>
            <p>This ist a search-tool for Music und Literature.</p>
            <p>Find matching music titles and artists for any search term in the iTunes and MusicBrainz databases. 
            The literature search shows matching books or publications from OpenLibrary.</p>
            <p>Build with Python & PySide6.</p>
            <p>Developed by Henriette Baum.</p>
            <p>Licensed under the MIT License.</p>
            <p>Copyright © 2026</p>
            """
        )

    # ----- Dark Mode -----
    def detect_dark_mode(self):
        # Fragt das System-Farbschema direkt ab (funktioniert ab Qt 6.5)
        hints = QGuiApplication.styleHints()
        return hints.colorScheme() == Qt.ColorScheme.Dark



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
                #orientation = QPageLayout.Orientation.Portrait
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



    def closeEvent(self, event):
        """Wird aufgerufen, wenn der User das Fenster schließt."""
        # Prüfen, ob der Worker existiert und noch läuft
        if hasattr(self, 'worker') and self.worker.isRunning():
            print("DEBUG: Suche läuft noch. Beende Thread vor dem Schließen...")
            
            # Den Thread bitten, aufzuhören
            self.worker.quit()
            
            # Maximal 2 Sekunden warten, ob er von alleine fertig wird
            if not self.worker.wait(2000):
                print("DEBUG: Thread reagiert nicht, erzwinge Abbruch.")
                self.worker.terminate()
                self.worker.wait() # Warten, bis er wirklich weg ist
    
        print("DEBUG: App will be closed.")
        event.accept() # Schließen zulassen
    