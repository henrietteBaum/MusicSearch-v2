# MusicSearch (v2.2.7)

**MusicSearch** ist eine barrierefreie Desktop-Anwendung zur gleichzeitigen Suche nach Musik (iTunes, MusicBrainz) und Literatur (OpenLibrary).

Im Gegensatz zu vielen Web-Interfaces legt diese App ihren Fokus konsequent auf **Benutzerzentrierung** und **Barrierefreiheit (A11y)**. Sie wurde entwickelt, um Screenreader-Nutzern und Menschen mit Sehbeeinträchtigungen ein stressfreies Rechercherlebnis zu ermöglichen.


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

**Linux (Ubuntu, Mint, Fedora):**

```bash
python3 -m venv .venv
source .venv/bin/activate

```

### 3. Abhängigkeiten installieren

```bash
pip install PySide6 requests

```

## System-spezifische Hinweise (Linux)

Sollte die App unter **Linux Mint** oder **Ubuntu** nicht starten (XCB-Fehler), fehlt eine wichtige Systembibliothek. Installieren Sie diese mit:

```bash
sudo apt update && sudo apt install libxcb-cursor0

```

Unter **Fedora** integriert sich die App nahtlos in die KDE-Umgebung und übernimmt Ihre gewählten Systemfarben automatisch.

---

## App starten

Starten Sie die Anwendung aus dem Hauptverzeichnis mit folgendem Befehl:

```bash
python -m main.py

```
## Versions-Highlights

* **v2.2.7:** Umstieg auf lokale Material Design Icons (Fallback-Sicherheit).
* **v2.2.5:** Einheitliches Datenmodell („Album“ statt API-Kryptik).
* **v2.1.4:** Umstellung auf semantische HTML-Ergebnisanzeige für Screenreader.
* **v2.0.0:** Erste stabile CLI-Version mit MusicBrainz-Integration.

---

## Das Team

Dieses Projekt ist eine Gemeinschaftsarbeit von:

* **Henriette** (Lead Developer)
* **Conrad** (Chief Morale Officer 🐕 – zuständig für Pausenmanagement)
* **Gemini & Lumo** (KI-Kollaborateure für Architektur & Code-Reviews)



