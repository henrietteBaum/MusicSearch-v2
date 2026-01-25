# README v2.1.4

 Barrierefreiheit (Accessibility) wird in der Softwareentwicklung oft unterschätzt. Die Zeitdauer zu erhöhen, ist genau die richtige Entscheidung, damit Nutzer stressfrei lesen können, was das Programm gerade getan hat.

Ein kleiner Tipp für später: Du kannst Nachrichten in der Statuszeile sogar mit HTML ein wenig hervorheben (z. B. fett schreiben), damit sie noch besser lesbar sind:
`self.statusBar().showMessage("<b>Datei wurde erfolgreich gespeichert!</b>", 8000)`

Da du jetzt los musst, hier eine kurze Zusammenfassung, was wir geschafft haben:

1. **Modularer Zugriff:** Dein `MainWindow` findet jetzt den `result_browser` in jedem beliebigen Tab.
2. **Intelligenter Pfad:** Die App schlägt "Dokumente" vor und merkt sich, wo du zuletzt warst.
3. **Sichere Dateinamen:** Mit Zeitstempel und Tab-Titel wird nichts mehr versehentlich überschrieben.
4. **Feedback:** Die Statuszeile gibt eine klare Rückmeldung mit genügend Zeit zum Lesen.


________________

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


## v2.2.6 - 2026-01-18
Weitere Anpassungen der Benutzeroberfläche zur Verbesserung der Lesbarkeit und Benutzerfreundlichkeit.
- der Search-Button wurde vergrößert und wird farblich hervorgehoben, sobald der Mauszeiger darüber schwebt (hover-Effekt).
- die Tab-Leiste wurde optisch überarbeitet, um die aktive Registerkarte besser hervorzuheben. Hier wurde ebenfalls ein hover-Effekt hinzugefügt. Und die Schriftgröße der Tab-Titel wurde leicht erhöht, um die Lesbarkeit zu verbessern.
- für die Icons der Toolbar wurden Fallback-Icons hinzugefügt, falls die Standard-Icons des Betriebssystems nicht verfügbar sind.

Die Anpassungen mithilfe der Datei `ui_styles.py` verändern zum Teil die Vorgaben von Qt für die Darstellung der Benutzeroberfläche.

Die App funktioniert mit diesen Änderungen insbesondere unter KDE-Plasma weiterhin wie gewohnt. Auf anderen Betriebssystemen und Desktops kann es vorkommen, dass die Icons der Toolbar nicht korrekt angezeigt werden, vor allem, wenn das Betriebssystem unter dem Namen des Standard-Icons ein anderes Icon vorsieht. Sobald ein zum vorgegebenen Namen passendes Icon gefunden wird, kommt das vorgesehende Fallback-Icon nicht zum Einsatz.

Auch mit der Farbgebung kann es Probleme geben. Bei unseren Tests funktionierte die App gut unter LinuxMint, Fedora-KDE, Fedora Workstation und Windows 11. Die vom Nutzer gewählte System-Farbgebung wird respektiert und der Dark-Mode wird übernommen. 

Unter Ubuntu 25.10 gab es jedoch Probleme mit der Farbgebung, die App wurde im Hellen Modus dargestellt, wodurch zum Teil die Schrift nicht mehr lesbar war.

Um solche Probleme zu beheben, können Sie in der Datei `ui_styles.py` die Farbwerte für die verschiedenen Elemente der Benutzeroberfläche anpassen. Die Datei ist gut kommentiert, sodass nan leicht erkennen kann, welche Farben für welche Elemente zuständig sind. 

