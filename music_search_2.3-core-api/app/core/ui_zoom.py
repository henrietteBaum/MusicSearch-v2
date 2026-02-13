# app/core/ui_zoom.py

from PySide6.QtCore import QObject, Qt, QEvent, Signal
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

class UIZoomFilter(QObject):
    
    # Sendet neuen Zoom-Faktor als Text für die Statusbar (optional)
    zoomChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.app = QApplication.instance()
        
        # Start-Schriftgröße merken
        self.default_font = self.app.font()
        self.base_size = self.default_font.pointSize()
        if self.base_size <= 0: 
            self.base_size = 10 # Fallback
            
        self.current_zoom = 1.0 # 1.0 = 100%

    def zoom_in(self):
        self.current_zoom += 0.1
        if self.current_zoom > 2.5: # Max 250%
            self.current_zoom = 2.5
        self.apply_zoom()

    def zoom_out(self):
        self.current_zoom -= 0.1
        if self.current_zoom < 0.5: # Min 50%
            self.current_zoom = 0.5
        self.apply_zoom()

    def reset_zoom(self):
        self.current_zoom = 1.0
        self.apply_zoom()

    def apply_zoom(self):
        # Neue Punktgröße berechnen
        new_size = max(6, int(self.base_size * self.current_zoom))
        
        # Auf die ganze App anwenden
        font = QFont(self.default_font)
        font.setPointSize(new_size)
        self.app.setFont(font)
        
        # Signal senden
        percent = int(self.current_zoom * 100)
        self.zoomChanged.emit(f"{percent}%")

    # Optional: Bonus-Feature (Strg+Shift+Mausrad für UI Zoom)
    # Wenn du das nicht willst, kannst du die Methode eventFilter auch löschen.
    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.Wheel:
            modifiers = event.modifiers()
            # Nur bei STRG + SHIFT reagieren (damit STRG+Wheel für den Content frei bleibt)
            if (modifiers & Qt.KeyboardModifier.ControlModifier and 
                modifiers & Qt.KeyboardModifier.ShiftModifier):
                
                if event.angleDelta().y() > 0:
                    self.zoom_in()
                else:
                    self.zoom_out()
                return True 
        return super().eventFilter(watched, event)