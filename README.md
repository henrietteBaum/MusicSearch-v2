# MusicSearch Version 2


<table>
  <tr>
    <td>
      <img src="assets/app-icon-orange-pink-circle.png" width="240">
    </td>
    <td>
      <h3> MusicSearch mit Python und PySide5 </h3>
      <p> MusicSearch ist eine barrierefreie Desktop-Anwendung zur gleichzeitigen Suche nach Musik (iTunes, MusicBrainz) und Literatur (OpenLibrary). 
      </p>
    </td>
  </tr>
</table>


Im Gegensatz zu vielen Web-Interfaces legt diese App ihren Fokus konsequent auf Benutzerzentrierung und Barrierefreiheit. Sie wurde entwickelt, um Screenreader-Nutzern und Menschen mit Sehbeeinträchtigungen ein stressfreies Rechercherlebnis zu ermöglichen.

MusicSearch ist als Lern- und Demo-Projekt für den Bereich Barrierefreiheit entstanden. Es kann als Vorlage dienen für Apps, die für den Nutzer API-Schnittstellen implementieren

![screenshot: MusicSearch v2.2.7](./assets/musicsearch-v2.2.7.png)


## Key Features (Accessibility First)

* **Semantische HTML-Ausgabe:** Ergebnisse werden im `QTextBrowser` strukturiert aufbereitet, sodass Screenreader Überschriften und Datensätze klar unterscheiden können.
* **Optimierte Tab-Führung:** Die Fokus-Reihenfolge folgt dem natürlichen Arbeitsfluss (Eingabe -> Filter -> Ergebnisse).
* **Grenzenloser Zoom:** Die Ergebnisanzeige lässt sich per `Strg + Mausrad` oder Tastatur flexibel skalieren.
* **Hoher Kontrast & Akzentfarben:** Die App verzichtet auf blasse Schriften und übernimmt automatisch die Akzentfarben Ihres Betriebssystems.
* **Plattform-Konsistenz:** Eigene Material Design Icons garantieren ein identisches Interface unter Windows, KDE und GNOME.


## Installation & Setup

Wir haben die Installation so einfach wie möglich gestaltet. Bitte folgen Sie den Schritten für Ihr System.

### 1. Projektordner vorbereiten

Laden Sie das Repository herunter und navigieren Sie im Terminal in den Hauptordner.

### 2. Virtuelle Umgebung einrichten (Empfohlen)

Um Konflikte mit anderen Python-Paketen zu vermeiden, nutzen wir ein `venv`.

**Windows 11:**

```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Linux (Ubuntu, Mint, Fedora, Mac):**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Abhängigkeiten installieren

```bash
pip3 install pyside6 requests
```

## System-spezifische Hinweise

Sollte die App unter **Linux Mint** oder **Ubuntu** nicht starten (XCB-Fehler), fehlt eine wichtige Systembibliothek. Installieren Sie diese mit:

```bash
sudo apt update && sudo apt install libxcb-cursor0
```

Unter **Fedora-KDE**, **LinuxMint**, **MacOS**, **Windows11** integriert sich die App nahtlos in die Desktop-Umgebung und übernimmt die gewählten Systemfarben automatisch.

Unter Fedora-Workstation 43 (GNOME) und Ubuntu 25.10 wird der DarkMode nicht übernommen. Dadurch sind die fest programmierten weißen Schriftfarben aus den App-Versionen 2.2.6 und 2.2.7 nicht lesbar. Verwenden Sie für diese Betriebssysteme Version 2.2.5, die noch keine Formatierung vorgibt.


## App starten

Starten Sie die Anwendung aus dem Hauptverzeichnis mit folgendem Befehl:

```bash
python3 main.py
```
## Versions-Highlights

- **v2.2.7:** Umstieg auf lokale Material Design Icons (Fallback-Sicherheit).
- **v2.2.5:** Einheitliches Datenmodell („Album“ statt API-Kryptik).
- **v2.2.0** Implementierung der OpenLibrary-API
- **v2.1.4:** Umstellung auf semantische HTML-Ergebnisanzeige für Screenreader.
- **v2.0.0:** Erste stabile CLI-Version mit iTunes und MusicBrainz-Integration.


