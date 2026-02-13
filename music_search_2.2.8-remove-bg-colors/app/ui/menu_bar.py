from PySide6.QtWidgets import QMenuBar, QMenu, QApplication
from PySide6.QtGui import QAction, QKeySequence, QPalette 
from PySide6.QtCore import Signal

from ui.ui_styles import get_menubar_css, get_accent_color

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

        #new_action = QAction("New", self)
        #open_action = QAction("Open", self)
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



        #self.addAction(view_menu.menuAction())
        # toggle_toolbar_action = QAction("Toggle Toolbar", self, checkable=True)
        # toggle_sidebar_action = QAction("Toggle Sidebar", self, checkable=True)
        # view_menu.addAction(toggle_toolbar_action)
        # view_menu.addAction(toggle_sidebar_action)
        # self.addMenu(view_menu)

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
        self.setStyleSheet(get_menubar_css(accent))

# ----- inside document -----

    # def apply_accessibility_style(self):
    #     """
    #     Erzwingt eine größere Schriftart für die Menüleiste,
    #     besonders wichtig unter Windows.
    #     """
    #     # Holen der Akzentfarbe des Systems (für Hover-Effekte)
    #     palette = self.palette()
    #     highlight_color = palette.color(QPalette.Highlight).name()

    #     # Wir nutzen 'pt' (Points) statt 'px', damit es sich besser an DPI-Einstellungen anpasst.
    #     # 11pt oder 12pt ist meist eine gute Größe für Accessibility (Standard ist oft 9pt).
        
    #     self.setStyleSheet(f"""
    #         /* Die Leiste selbst */
    #         QMenuBar {{
    #             font-size: 12pt;
    #             font-family: 'Segoe UI', sans-serif; /* Gute Windows-Schrift */
    #         }}

    #         /* Die einzelnen Einträge in der Leiste (File, Edit...) */
    #         QMenuBar::item {{
    #             padding: 6px 12px; /* Mehr Platz zum Klicken/Lesen */
    #             background: transparent;
    #         }}

    #         /* Hover-Effekt für die Leiste (wichtig für Orientierung) */
    #         QMenuBar::item:selected {{
    #             background: rgba(0, 0, 0, 0.1); /* Leichtes Grau beim Drüberfahren */
    #             border-radius: 4px;
    #         }}

    #         /* Die aufgeklappten Menüs (Dropdowns) */
    #         QMenu {{
    #             font-size: 12pt;
    #             padding: 5px; /* Etwas Luft am Rand des Fensters */
    #             /* border: 1px solid {highlight_color};  Rahmen hilft bei Sehschwäche */
    #         }}

    #         /* Die Einträge im Dropdown */
    #         QMenu::item {{
    #             padding: 6px 25px 6px 10px; /* Rechts viel Platz für Shortcuts lassen */
    #             margin: 2px; /* Abstand zwischen Einträgen verhindert Verrutschen */
    #         }}

    #         /* Hover im Dropdown (wichtig: hohe Kontraste nutzen!) */
    #         QMenu::item:selected {{
    #             background-color: {highlight_color};  /* Akzentfarbe */
    #             color: white;
    #         }}
    #     """)


        

       