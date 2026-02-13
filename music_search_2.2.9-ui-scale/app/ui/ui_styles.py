# app/ui/ui_styles.py

from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget

from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtCore import QSize

def get_accent_color(widget: QWidget) -> str:
    """Gibt den Hex-String der Akzentfarbe zurück (z.B. #3498db)."""
    return widget.palette().color(QPalette.Highlight).name()

def get_transparent_accent(hex_color: str, opacity: float) -> str:
    """
    Wandelt Hex (#RRGGBB) in rgba(r, g, b, opacity) um.
    opacity: 0.0 (durchsichtig) bis 1.0 (voll).
    Das verhindert Farbfehler bei Transparenz.
    """
    c = QColor(hex_color)
    # Rückgabeformat: rgba(120, 63, 119, 0.1)
    return f"rgba({c.red()}, {c.green()}, {c.blue()}, {opacity})"

# --- TOOLBAR ---
def get_toolbar_css(accent_color: str, scale: float = 1.0) -> str:
    border_bottom = int(3 * scale)
    padding_b = int(4 * scale)
    padding_lr = int(8 * scale)
    margin = int(2 * scale)
    
    # Wir berechnen die transparenten Farben sicher via rgba
    hover_bg = get_transparent_accent(accent_color, 0.1)   # 10% Deckkraft
    checked_bg = get_transparent_accent(accent_color, 0.15) # 15% Deckkraft

    return f"""
        QToolBar {{
            spacing: {int(10 * scale)}px;
            border: none;
            background: transparent; 
        }}
        QToolButton {{
            background: transparent; 
            border: none;
            border-bottom: {border_bottom}px solid transparent; 
            padding-bottom: {padding_b}px;
            padding-left: {padding_lr}px;
            padding-right: {padding_lr}px;
            margin: {margin}px;
        }}
        QToolButton:checked {{
            border-bottom: {border_bottom}px solid {accent_color};
            background-color: {checked_bg}; 
            font-weight: bold;
        }}
        QToolButton:hover {{
            background-color: {hover_bg}; 
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


# --- SIDEBAR BUTTON ---
def get_search_button_css(accent_color: str, scale: float = 1.0) -> str:
    font_size = int(11 * scale)
    padding_v = int(8 * scale)
    padding_h = int(16 * scale)
    radius = int(4 * scale)

    hover_bg = get_transparent_accent(accent_color, 0.15)

    return f"""
        QPushButton {{
            border: 1px solid palette(mid); 
            border-radius: {radius}px;
            padding: {padding_v}px {padding_h}px;
            font-size: {font_size}pt;
            font-weight: bold;
            background-color: transparent; /* Oder palette(button) */
        }}
        QPushButton:hover {{
            border: 2px solid {accent_color};
            background-color: {hover_bg}; 
        }}
        QPushButton:pressed {{
            background-color: {accent_color};
            /* Sicherstellen, dass Text auf der Akzentfarbe lesbar ist */
            color: palette(highlighted-text); 
            border: 2px solid {accent_color};
        }}
        QPushButton:disabled {{
            border: 1px solid palette(midlight);
            color: palette(mid);
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

# --- TABS ---
def get_tab_widget_css(accent_color: str, scale: float = 1.0) -> str:
    font_size = int(11 * scale)
    padding_v = int(10 * scale)
    padding_h = int(20 * scale)
    border_w = int(3 * scale)

    selected_bg = get_transparent_accent(accent_color, 0.1)
    hover_bg = get_transparent_accent(accent_color, 0.05)

    return f"""
        QTabWidget::pane {{
            border: none;
            border-top: 1px solid palette(mid);
            background: transparent;
        }}
        QTabBar {{
            background: transparent;
        }}
        QTabBar::tab {{
            background: transparent;
            padding: {padding_v}px {padding_h}px;
            margin-right: 2px;
            border-bottom: {border_w}px solid transparent;
            font-size: {font_size}pt;
        }}
        QTabBar::tab:selected {{
            border-bottom: {border_w}px solid {accent_color};
            font-weight: bold;
            /* Textfarbe: Akzentfarbe für Text, falls gewünscht */
            color: {accent_color}; 
            background-color: {selected_bg};
        }}
        QTabBar::tab:hover:!selected {{
            background-color: {hover_bg};
            border-bottom: {border_w}px solid palette(mid);
        }}
        QTabBar::tab:focus {{
            border: 1px dotted {accent_color};
        }}
    """

# --- MENUBAR ---
def get_menubar_css(accent_color: str, scale: float = 1.0) -> str:
    font_size = int(11 * scale)
    pad_item_v = int(6 * scale)
    pad_item_h = int(12 * scale)
    
    hover_bg = get_transparent_accent(accent_color, 0.15)

    return f"""
        QMenuBar {{
            font-size: {font_size}pt;
            font-family: 'Segoe UI', sans-serif;
            background: transparent;
        }}
        QMenuBar::item {{
            padding: {pad_item_v}px {pad_item_h}px;
            background: transparent;
        }}
        
        QMenuBar::item:selected {{
            background: {hover_bg};
            border-bottom: 2px solid {accent_color};
        }}

        QMenu {{
            font-size: {font_size}pt;
            padding: 5px;
            border: 1px dotted {accent_color};
            /* Kein Background definiert -> Systemstandard */
        }}
        QMenu::item {{
            padding: 6px 25px 6px 10px;
            margin: 2px;
        }}
        
        QMenu::item:selected {{
            background-color: {accent_color};
            color: palette(highlighted-text);
        }}
    """