from PySide6.QtWidgets import QMenuBar, QMenu, QApplication
from PySide6.QtGui import QAction, QKeySequence, QPalette 
from PySide6.QtCore import Signal

from ui.ui_styles import get_menubar_css, get_accent_color
from ui.icons import IconManager

class MenuBar(QMenuBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_menus()

        # --- HIER: Stylesheet für bessere Lesbarkeit ---
        self.apply_styles()

    def _build_menus(self):
        file_menu = self.addMenu("&File")
        # file_menu = QMenu("File", self)
        # self.addAction(file_menu.menuAction())

        self.save_action = QAction("&Save", self)
        self.export_pdf_action = QAction("&Export to PDF", self)
        self.print_action = QAction("&Print", self)
        exit_action = QAction("E&xit", self)

        file_menu.addAction(self.save_action)
        file_menu.addAction(self.export_pdf_action)
        file_menu.addAction(self.print_action)

        file_menu.addSeparator()
        
        file_menu.addAction(exit_action)
        exit_action.triggered.connect(QApplication.instance().quit)


        # View Menu
        view_menu = QMenu("&View", self)
        
        #self.zoom_in_action = QAction("Zoom &In", self)
        #self.zoom_in_action.setShortcut(QKeySequence.StandardKey.ZoomIn)
        
        # ----- Zoom In -----
        self.zoom_in_action = QAction(IconManager.get_icon("zoom-in", "zoom_in.svg"), "Zoom In (UI)", self)
        # Standard Shortcut für Zoom In (meist Strg++)
        self.zoom_in_action.setShortcut(QKeySequence.ZoomIn) 
        view_menu.addAction(self.zoom_in_action)


        #self.zoom_out_action = QAction("Zoom &Out", self)
        #self.zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut)

        # ----- Zoom Out -----
        self.zoom_out_action = QAction(IconManager.get_icon("zoom-out", "zoom_out.svg"), "Zoom Out (UI)", self)
        # Standard Shortcut für Zoom Out (meist Strg+-)
        self.zoom_out_action.setShortcut(QKeySequence.ZoomOut)
        view_menu.addAction(self.zoom_out_action)


        #self.reset_zoom_action = QAction("&Reset Zoom", self)
        #self.reset_zoom_action.setShortcut(QKeySequence("Ctrl+0"))

        # ----- Reset -----
        self.reset_zoom_action = QAction(IconManager.get_icon("zoom-original", "center_focus_strong.svg"), "Reset Zoom", self)
        self.reset_zoom_action.setShortcut("Ctrl+0")
        view_menu.addAction(self.reset_zoom_action)

        view_menu.addAction(self.zoom_in_action)
        view_menu.addAction(self.zoom_out_action)
        view_menu.addAction(self.reset_zoom_action)


        # Help Menu
        help_menu = self.addMenu("&Help")
        self.help_action = QAction("Documentation", self)
        help_menu.addAction(self.help_action)
        help_menu.addSeparator()
        self.about_action = QAction("About", self)
        help_menu.addAction(self.about_action)


        # ----- Add Menus to the Menu Bar -----
        self.addMenu(file_menu)
        self.addMenu(view_menu)
        self.addMenu(help_menu)


# ----- Accessibility Styles for MenuBar -----
    def apply_styles(self):
        accent = get_accent_color(self)
        # Hier brauchen wir keine Farbe übergeben
        #self.setStyleSheet(get_menubar_css(accent))   
        self.setStyleSheet(get_menubar_css(accent))       