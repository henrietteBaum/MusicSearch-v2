# App-UI zoom mit PySide6

Die Datei app/core/ui_zoom.py ist technisch gesehen das "Gehirn" der Skalierung. Sie enthält die Qt-Konzepte EventFilter, QApplication-Instanz.


```python
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
```

## Erläuterung:

Die Aufgabe der Klasse UIZoomFilter:

Diese Klasse ist ein unsichtbarer "Helfer", der im Hintergrund läuft. Sie hat zwei Hauptaufgaben:

Steuerung: Sie berechnet die neue Schriftgröße basierend auf einem Zoom-Faktor (z.B. 1.2 für 120%).

Überwachung (Event Filter): Sie klinkt sich in den Nachrichtenstrom der Anwendung ein und lauscht auf spezielle Tastatur-Maus-Kombinationen (Strg + Shift + Mausrad), um den Zoom auszulösen.


```python
class UIZoomFilter(QObject):
    
    # Signal sendet den neuen Zoom-Faktor als Text (z.B. "120%") an die UI
    zoomChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # Wir holen uns Zugriff auf die laufende Anwendung (das ganze Programm)
        self.app = QApplication.instance()
        

```

`QObject`: Die Basisklasse für fast alles in Qt. Wir erben davon, damit wir Signals benutzen können.

`QApplication.instance()`: Damit greifen man auf das globale Anwendungsobjekt zu. Das wird später benötigt, um die Schriftart für alle Fenster gleichzeitig zu ändern.


## Singleton

Eine Qt-Anwendung (QApplication) ist ein sogenanntes Singleton. Das bedeutet: Es darf technisch gesehen in deinem ganzen Programm nur eine einzige Instanz davon geben. Das ist der "Chef" des Programms.

Aber Klasse UIZoomFilter lebt in einer ganz anderen Datei (app/core/ui_zoom.py). Die Klasse UIZoomFilter kennt die Variable app aus der main.py nicht (Variable Scope). 

Sobald man irgendwo QApplication(...) aufruft, merkt sich Qt dieses Objekt intern in einer globalen, statischen Variable.

QApplication.instance() liefert genau das Objekt zurück, das in der main.py in der Variable app gespeichert ist.

`QApplication(sys.argv)`: Erstellt das Anwendungsobjekt (den "Chef") und startet die Event-Verarbeitung. Das passiert in main.py.

`QApplication.instance()`: Eine statische Methode, die von überall im Code aufgerufen werden kann. Sie liefert einen Verweis (Pointer) auf genau dieses eine Anwendungsobjekt zurück.

Um in der Datei ui_zoom.py Zugriff auf globale Einstellungen (wie setFont) zu haben, ohne die app-Variable aus der main.py mühsam durchreichen zu müssen.

Bildlich gesprochen:

`main.py`: Stellt den Geschäftsführer ein (app = ...).

`ui_zoom.py`: Ist ein Mitarbeiter in einer anderen Abteilung, der eine Durchsage machen will. Er weiß nicht, wie der Geschäftsführer heißt, aber er ruft instance() ("Zentrale, verbinde mich mit dem Chef!"), und Qt verbindet ihn automatisch mit dem Objekt aus main.py


```python
self.default_font = self.app.font()
self.base_size = self.default_font.pointSize()
```


`base_size` : die Schriftgröße wird beim Start gespeicher. Wenn wir zoomen, berechnen wir immer von dieser Basis * Faktor. Würden wir stattdessen immer die aktuelle Größe nehmen (Aktuell * 1.1), würde die Schrift durch Rundungsfehler irgendwann krumm werden.

`self.app.font()`:

Holt das aktuelle Standard-Schrift-Objekt (QFont) der gesamten Anwendung. Dieses Objekt enthält alle Eigenschaften wie Schriftart-Familie ("Arial"), Dicke und Größe.

`.pointSize()`:

Liest aus dem Schrift-Objekt die aktuelle Größe in Punkten (pt) aus.

Hinweis: Wir nutzen Punkte (pt) statt Pixel (px), da Punkte auf hochauflösenden Bildschirmen (High-DPI) automatisch richtig skalieren. Ein Punkt ist im Druckwesen 1/72 Zoll.

Rückgabewert ist ein int (z.B. 10).

Die Berechnung:

    Wir nehmen die Basisgröße (z.B. 10 pt).

    Wir multiplizieren mit dem Faktor (z.B. 1.2 für 120%).

    Ergebnis: 10 * 1.2 = 12.

Anschließend wird ein neues Font-Objekt erstellt und dort die Schriftgröße gesetzet: `new_font.setPointSize(12)`.



```python
# Fallback, falls das Betriebssystem keine Größe liefert
if self.base_size <= 0: 
    self.base_size = 10 
            
self.current_zoom = 1.0 # Startwert: 1.0 entspricht 100%
```

Spezialfall (Fallback):
Der Code enthält die Zeile `if self.base_size <= 0`.
Das ist wichtig, weil manche Systeme Schriften in Pixeln definieren. In diesem Fall würde pointSize() den Wert -1 zurückgeben (Fehler). Wir fangen das ab und setzen einen Standardwert (10).

## eventFilter

Das ist der komplexeste Teil der Datei. Ein eventFilter ist wie ein Pförtner, der Post abfängt, bevor sie beim Empfänger ankommt.


```python
def eventFilter(self, watched, event):
        # Wir interessieren uns nur für Mausrad-Bewegungen (Wheel)
        if event.type() == QEvent.Type.Wheel:
            
            # Welche Tasten werden gerade gedrückt gehalten?
            modifiers = event.modifiers()
            
            # Bitweise Prüfung: Ist STRG (Control) UND SHIFT gedrückt?
            if (modifiers & Qt.KeyboardModifier.ControlModifier and 
                modifiers & Qt.KeyboardModifier.ShiftModifier):
                
                # angleDelta().y() > 0 bedeutet: Rad nach oben gedreht (weg vom User)
                if event.angleDelta().y() > 0:
                    self.zoom_in()
                else:
                    self.zoom_out()
                
                # return True bedeutet: "Ich habe das Event verarbeitet!"
                # Das Event wird NICHT weitergeleitet. Das Scrollen findet also nicht statt.
                return True 
        
        # Alle anderen Events (Klicks, Tasten ohne Shift, etc.) lassen wir passieren.
        return super().eventFilter(watched, event)
```

Event Filter: In Qt kann ein Objekt die Events eines anderen überwachen. Wir installieren diesen Filter später auf der QApplication, damit er alle Mausrad-Events der ganzen App sieht.

Modifiers: Wir prüfen auf Strg + Shift. Das ist wichtig, weil Strg + Mausrad (ohne Shift) oft schon vom QTextBrowser für den Inhalt-Zoom benutzt wird. Wir wollen uns nicht gegenseitig stören.

- Return True vs super():

True: Stopp! Das Event ist erledigt. (Verhindert, dass man versehentlich im Fenster scrollt, während man zoomt).

super()...: Weitermachen. Das Event wird normal verarbeitet.

`super()` sorgt dafür, dass die normale Funktionalität der App nicht blockiert wird, während der Filter auf die speziellen Tastenkombinationen lauschst.

Vererbung: Deine Klasse UIZoomFilter erbt von QObject.

Überschreiben (Overriding): die Methode `eventFilter` wird neu definiert. Damit wird die Standard-Methode von QObject "verdeckt".

Nicht behandelte Ereignisse werden an die Funktion eventFilter() der Basisklasse weitergeleitet, da die Basisklasse eventFilter() möglicherweise für ihre eigenen internen Zwecke neu implementiert hat.

Der Standard-Weg: Die originale QObject.eventFilter-Methode macht standardmäßig meistens nichts anderes, als False zurückzugeben (was bedeutet: "Event ignorieren, lass es weiter zum Ziel-Widget laufen").

Würde man von einer komplexeren Klasse als QObject erben, die wichtige Aufgaben im eventFilter ausführt, würde man diese Aktionen sonst kaputt machen.


```python
def zoom_in(self):
        self.current_zoom += 0.1  # Erhöhe um 10%
        # Begrenzung (Clamping): Nicht größer als 250%
        if self.current_zoom > 2.5: 
            self.current_zoom = 2.5
        self.apply_zoom()

def zoom_out(self):
    self.current_zoom -= 0.1  # Verringere um 10%
    # Begrenzung: Nicht kleiner als 50%
    if self.current_zoom < 0.5: 
        self.current_zoom = 0.5
    self.apply_zoom()
```

Hier wird nur der Faktor (self.current_zoom) mathematisch verändert.

Die if-Abfragen verhindern, dass die UI unbenutzbar riesig oder winzig wird.


```python
def apply_zoom(self):
        # 1. Berechne neue Schriftgröße (z.B. 10pt * 1.2 = 12pt)
        # max(6, ...) verhindert, dass die Schrift unsichtbar klein wird (Schutzmechanismus)
        new_size = max(6, int(self.base_size * self.current_zoom))
        
        # 2. Erstelle eine Kopie der Standard-Schriftart und setze die neue Größe
        new_font = QFont(self.default_font)
        new_font.setPointSize(new_size)
        
        # 3. WICHTIG: Setze diese Schriftart GLOBAL für die ganze App.
        # Alle Widgets, die keine eigene feste Schriftart haben, erben diese Einstellung sofort.
        self.app.setFont(new_font)
        
        # 4. Informiere den Rest der App (z.B. MainWindow), dass sich der Zoom geändert hat.
        # Wir senden einen String (z.B. "120%"), der in der Statusbar angezeigt werden kann.
        percent = int(self.current_zoom * 100)
        self.zoomChanged.emit(f"{percent}%")
```

`self.app.setFont(new_font)`: Das ist der mächtigste Befehl hier. Er ändert den "Standard" der Anwendung. Da fast alle unsere Widgets (Buttons, Labels, Menüs) auf dem Standard basieren, wachsen oder schrumpfen sie automatisch mit.

`self.zoomChanged.emit(...)`: Da wir hier in einer separaten Klasse sind ("Backend"), dürfen wir nicht direkt auf die Statusbar zugreifen. Stattdessen "rufen" wir (Signal), und das MainWindow "hört" (Slot) und aktualisiert dann die Stylesheets und die Statusbar.

___


## Für die einzelnen Widgets in der Datei `ui_styles.py`:
- die Methoden zur Formatierung der einzelnen Widgets erhalten den Anfangswerdet `scale` als float-Parameter, mit dem default-Wert 1.0
- die Werte für die Skalierung werden in int-Werte umgewandelt, mit einem Skalierungsfaktor multipliziert und in einer Variablen gespeichert, jeweils für die einzelnen Elemente angepasst



```python
# ...

def get_toolbar_css(accent_color: str, scale: float = 1.0) -> str:
    border_bottom = int(3 * scale)
    padding_b = int(4 * scale)
    padding_lr = int(8 * scale)
    margin = int(2 * scale)

# ...
```


```python
# ...

def get_search_button_css(accent_color: str, scale: float = 1.0) -> str:
    font_size = int(11 * scale)
    padding_v = int(8 * scale)
    padding_h = int(16 * scale)
    radius = int(4 * scale)

# ...
```


```python
# ...

def get_tab_widget_css(accent_color: str, scale: float = 1.0) -> str:
    font_size = int(11 * scale)
    padding_v = int(10 * scale)
    padding_h = int(20 * scale)
    border_w = int(3 * scale)

# ...
```


```python
# ...

def get_menubar_css(accent_color: str, scale: float = 1.0) -> str:
    font_size = int(11 * scale)
    pad_item_v = int(6 * scale)
    pad_item_h = int(12 * scale)

# ...
```

Die so gespeicherten (und berechneten) Werte kann man dann einfach innerhalb eines f-Strings für die Formatierung der einzelnen Bereich verwenden, z.B. für Innenabstände als festen px-Wert und für die Schriftgrö0e als pt-Wert:


```python
padding: {padding_v}px {padding_h}px;

font-size: {font_size}pt;
```


```python
# ...
return f"""
    QPushButton {{
        border: 1px solid palette(mid); 
        border-radius: {radius}px;
        padding: {padding_v}px {padding_h}px;
        font-size: {font_size}pt;
        font-weight: bold;
        background-color: transparent; /* Oder palette(button) */
    }}
# ...
```

## In der Datei `main_window.py`

- werden die Methoden zur Formatierung aus der `ui_styles.py` importiert
- der aktuelle Zoom in der Variablen `scale` gespeichert
- diese wird dann an als Parameter an die jeweiligen Formatierungs-Methoden für die einzelnen Widgets übergeben
- die Formatierungs-Methoden werden von `setStylesheet()` aufgerufen


```python
# app/windows/main_window.py

from ui.ui_styles import (
    get_accent_color, get_menubar_css, get_toolbar_css,
    get_search_button_css, get_tab_widget_css
)

```

Zoom Steuerung über das Menü `View`:


```python
# Die Menü-Aktionen (und damit auch Strg++ / Strg+-) steuern jetzt den UI-Zoom
self.menu_bar.zoom_in_action.triggered.connect(self.ui_zoom.zoom_in)
self.menu_bar.zoom_out_action.triggered.connect(self.ui_zoom.zoom_out)
self.menu_bar.reset_zoom_action.triggered.connect(self.ui_zoom.reset_zoom)

# Optional: Feedback in Statusbar
self.ui_zoom.zoomChanged.connect(
    lambda val: self.statusBar().showMessage(f"UI Zoom: {val}", 8000)
)
```

Den Skalierungs-Faktor auf die Elemente anwenden:


```python

# ...


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

        # --- 2. MENUBAR  (Braucht accent UND scale) ---
        self.menu_bar.setStyleSheet(get_menubar_css(accent, scale))

        # --- 3. SIDEBAR BUTTON (Braucht accent UND scale) ---
        self.side_bar.search_button.setStyleSheet(get_search_button_css(accent, scale))

        # --- 4. TABS (Braucht accent UND scale) ---
        self.central_widget.all_tabs.setStyleSheet(get_tab_widget_css(accent, scale))
        
# ...


```

Die Methode `setStylesheet()` 

Stylesheets bestehen aus einer Abfolge von Stilregeln. Eine Stilregel besteht aus einem Selektor und einer Deklaration. Der Selektor gibt an, welche Widgets von der Regel betroffen sind; die Deklaration gibt an, welche Eigenschaften auf dem Widget festgelegt werden sollen.

Als Selektor verwenden wir hier das Widget selbst (class-Selektor) z.B. `self.menu_bar` und wenden darauf die Methode an:
`self.menu_bar.setStylesheet()`.

An diese Methode wiederum werden unsere eigenen, in der Datei `ui_styles.py` definierten Methoden übergeben, z.B.:
`self.menu_bar.setStylesheet(get_memubar_css())`

Die Methode `get_menubar_css()` wiederum gibt einen f-String zurück - und übergibt ihn damit an die aufrufende Methode `setStylesheet()`, zusammen mit ihren Parametern `accent, scale`. Der Inhalt des f-Strings entspricht weitestgehend der bekannten CSS-Syntax.
