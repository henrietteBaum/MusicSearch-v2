# README v2.2.6

Update Ui and Toolbar Icons


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

