# app/ui/styles.py

from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtCore import QSize


def get_accent_color(widget: QWidget) -> str:
    """
    Holt die Akzentfarbe (Highlight) vom System/Widget und gibt sie als Hex-String zurück.
    """
    palette = widget.palette()
    return palette.color(QPalette.Highlight).name()

# ----- ToolBar -----
def get_toolbar_css(accent_color: str) -> str:
    return f"""
        QToolBar {{
            spacing: 10px;
            border: none;
            background: transparent;
        }}
        QToolButton {{
            background-color: transparent; 
            border: none;
            border-bottom: 3px solid transparent; 
            padding-bottom: 4px;
            padding-left: 8px;
            padding-right: 8px;
            margin: 2px;
        }}
        QToolButton:checked {{
            border-bottom: 3px solid {accent_color};
            background-color: rgba(255, 255, 255, 0.05);
            font-weight: bold;
        }}
        QToolButton:hover {{
            background-color: rgba(255, 255, 255, 0.1);
        }}
    """

# ----- ToolBar Icons -----
def tint_icon(icon: QIcon, color_str: str, size: int = 28) -> QIcon:
    """Nimmt ein QIcon und färbt es komplett in der übergebenen Farbe um."""
    # Pixmap in der gewünschten Größe generieren
    pixmap = icon.pixmap(QSize(size, size))
    
    if pixmap.isNull():
        return icon

    painter = QPainter(pixmap)
    
    # KORREKTUR: Zugriff über QPainter.CompositionMode
    # Wir nutzen CompositionMode_SourceIn, um nur die Alpha-Maske zu füllen
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), QColor(color_str))
    painter.end()

    return QIcon(pixmap)



# ----- SideBar Button -----
def get_search_button_css(accent_color: str) -> str:
    return f"""
        QPushButton {{
            background-color: rgba(255, 255, 255, 0.08);
            border: 1px solid #555;
            border-radius: 4px;
            padding: 4px 8px;
            font-size: 12pt;
            font-weight: bold;
        }}
        QPushButton:hover {{
            border: 2px solid {accent_color};
            background-color: rgba(255, 255, 255, 0.15);
        }}
        QPushButton:pressed {{
            background-color: {accent_color};
            border: 2px solid {accent_color};
        }}
        QPushButton:disabled {{
            background-color: transparent;
            border: 1px solid #333;
            color: #666;
        }}
    """

# ----- SideBar Separator -----
def get_sidebar_separator_css(accent_color: str) -> str:
    return f"""
        #sidebarLine {{
            border: none;
            border-top: 1px solid {accent_color};
            background-color: transparent;
            max-height: 1px;
            margin-left: 4px;
            margin-right: 4px;
        }}
    """


# ----- Tabs (Central Widget) ----
def get_tab_widget_css(accent_color: str) -> str:
    return f"""
        QTabWidget::pane {{
            border: none;
            border-top: 1px solid #444;
            background: transparent;
        }}
        QTabBar {{
            background: transparent;
        }}
        QTabBar::tab {{
            background: transparent;
            padding: 10px 20px;
            margin-right: 2px;
            border-bottom: 3px solid transparent;
            font-size: 11pt;
        }}
        QTabBar::tab:selected {{
            border-bottom: 3px solid {accent_color};
            /* color: {accent_color};  <-- Optional, falls gewünscht */
            font-weight: bold;
            background-color: rgba(255, 255, 255, 0.05);
        }}
        QTabBar::tab:hover:!selected {{
            background-color: rgba(255, 255, 255, 0.1);
            border-bottom: 3px solid rgba(255, 255, 255, 0.3);
        }}
        QTabBar::tab:focus {{
            border: 1px dotted {accent_color};
        }}
    """

# ----- MenuBar (Windows Fix) -----
def get_menubar_css(accent_color: str) -> str:
    return (f"""
        QMenuBar {{
            font-size: 12pt;
            font-family: 'Ubuntu', 'Segoe UI', sans-serif;
        }}
        QMenuBar::item {{
            padding: 6px 12px;
            background: transparent;
        }}
        QMenuBar::item:selected {{
            background: gba(255, 255, 255, 0.1); 
            border-radius: 4px;
        }}
        QMenu {{
            font-size: 12pt;
            padding: 5px;
            border: 1px solid #555;
            /* background-color: #2A2D30; Sicherstellen, dass Hintergrund dunkel ist */
        }}
        QMenu::item {{
            padding: 6px 25px 6px 10px;
            margin: 2px;
        }}
        QMenu::item:selected {{
            background-color: {accent_color};  /* Akzentfarbe */
        }}
    """)