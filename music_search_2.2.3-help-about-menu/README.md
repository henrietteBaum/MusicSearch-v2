# README v2.1.4

 Barrierefreiheit (Accessibility) wird in der Softwareentwicklung oft unterschätzt. Die Zeitdauer zu erhöhen, ist genau die richtige Entscheidung, damit Nutzer stressfrei lesen können, was das Programm gerade getan hat.

Ein kleiner Tipp für später: Du kannst Nachrichten in der Statuszeile sogar mit HTML ein wenig hervorheben (z. B. fett schreiben), damit sie noch besser lesbar sind:
`self.statusBar().showMessage("<b>Datei wurde erfolgreich gespeichert!</b>", 8000)`

Da du jetzt los musst, hier eine kurze Zusammenfassung, was wir geschafft haben:

1. **Modularer Zugriff:** Dein `MainWindow` findet jetzt den `result_browser` in jedem beliebigen Tab.
2. **Intelligenter Pfad:** Die App schlägt "Dokumente" vor und merkt sich, wo du zuletzt warst.
3. **Sichere Dateinamen:** Mit Zeitstempel und Tab-Titel wird nichts mehr versehentlich überschrieben.
4. **Feedback:** Die Statuszeile gibt eine klare Rückmeldung mit genügend Zeit zum Lesen.


## Version 2.2.3

Über das Menü "Help" öffnet sich nun ein separates Fenster für die Dokumentation, der Menüpunkt "About" zeigt ein Info-Fenster mit Versionsnummer und Autoreninformationen an. Das Fenster für die Dokumentation lässt sich verschieben und in der Größe anpassen. Es kann neben dem Hauptfenster geöffnet bleiben, um während der Nutzung der Anwendung schnell auf die Hilfe zugreifen zu können.
Zusätzlich haben wir die Anzeige der Suchergebnisse optimiert durch eine deutlichere Trennung der einzelnen Datensätze im Ergebnisfenster. Eine horizontale Linie trennt nun die einzelnen Suchergebnisse, was die Lesbarkeit erheblich verbessert.
