# README v2.2.8


## v2.2.4 - 2026-01-17

- Korrektur: close-Fuktion und Thread-Fehler bein Schliessen des Fensters bei gleichzeitigem Verlassen des limit-Eingabefeldes behoben.
- Verbesserung der Lesbarkeit der Suchergebnisse durch Anpassung von Schriftgrößen und Abständen im Ergebnis-Browser, farbliche Trenner zwischen den Ergebnissen hinzugefügt.


## v.2.2.5 - 2026-01-17

Das ist ein wichtiges Prinzip im Software-Design: Das Model bestimmt die einheitliche Sprache deiner App, nicht die API.

    Für den User ist es ein "Album".

    iTunes nennt es technisch collectionName.

    MusicBrainz nennt es technisch releases.

    Spotify nennt es wieder anders.

Die Aufgabe deiner Service-Dateien (musicbrainz.py, itunes.py) ist es, diese fremden Begriffe in deine Sprache (album) zu übersetzen. Wenn du für jede API ein eigenes Feld machst (itunes_album, mb_release, spotify_context), wird dein Model riesig und dein Code für die Anzeige (Formatter) ein Chaos aus if/else.


## LinuxMint
installieren: libxcb-cursor0


## v2.2.7 - 2026-02-14
Um die Probleme mit den Icons der Toolbar zu beheben, haben wir die Fallback-Icons als Standard gesetzt. Dadurch wird sichergestellt, dass die Toolbar-Icons immer korrekt angezeigt werden, unabhängig von der Verfügbarkeit der System-Icons. Verwendet werden Icons der Material Design Icons Sammlung, die eine breite Palette von Symbolen bietet und gut mit verschiedenen Themes harmoniert. Die Icons wurden in das Projektverzeichnis unter `assets/toolbar_icons/` hinzugefügt und werden nun standardmäßig geladen.

## v2.2.8
`ui_styles.py`: 
- alle Formatierungen für die Schriftfarbe `color` entfernt.
- die Hintergrundfarbe im geöffneten Menü entfernt
- die Toolbar-Icons werden nun in der Akzentfarbe dargestellt
- für die Anzeige der Suchergebnisse haben wir Zeilenhöhe, den Abstand der Buchstaben und die Strichdicke angepasst.


### Icons

in der tool_bar.py

```python
  def apply_styles(self):
        # 1. Farbe holen
        accent = get_accent_color(self)
        # 2. CSS holen und setzen
        # self.setStyleSheet(get_toolbar_css(accent))

        # Alle Actions durchlaufen und Icons "einfärben"
        for action in self.actions():
            if not action.isSeparator():
                old_icon = action.icon()
                # Hier nutzen wir die korrigierte Funktion
                new_icon = tint_icon(old_icon, accent, 28)
                action.setIcon(new_icon)

        # 3. CSS für Layout und Unterstreichung setzen
        self.setStyleSheet(get_toolbar_css(accent))

```
in ui_styles.py

```python
# ...

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

# ...
```
## v2.2.9

main.py:

```python
 # ----- 1. Wayland-Support für Fedora/Ubuntu (GNOME) -----
    # Das hilft, damit die App nicht über XWayland "verschwommen" gerendert wird
    if sys.platform == "linux":
        os.environ["QT_QPA_PLATFORM"] = "wayland;xcb"

    # 2. Skalierungs-Logik für Qt 6
    # AA_EnableHighDpiScaling wird nicht mehr gebraucht, da in Qt 6 Standard!
    
    # Die Rundungspolicy ist wichtig für 125% oder 150% Skalierung
    # Wichtig: QGuiApplication kommt aus QtGui!
    QtGui.QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

```

## v2.2.9.2

Die UI kann nun per Tastenkombination vergrößert werdn. Wir verwenden die Menüpunkte `View - Zoom ...` sowie die Standard Tastenkombination `Strg + +` jetzt nur noch für die UI, nicht mehr separat für die Suchergebnisse im QTextBrowser. Diese kann der Benutzer weiterhin mit Mousewheel-Zoom beliebig vergrößern und verkleinern. 

Für die Hervorhebungen setzen wir die Akzentfarbe zum Teil in transparenter Form ein.
