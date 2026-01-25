# README v2.2.5

Add a media type ComboBox to select Album, Track, or Artist search.
The MusicBrainz search now also shows the Album for the search term.
Update the Search Function for OpenLibrary to show book-title and author from the users search term.
________________


## v.2.2.5 - 2026-01-17

Diese Version fügt eine weitere ComboBox hinzu, über die der Nutzer auswählen kann, welchen Medientyp er suchen möchte (Album, Track, Künstler).

Die Suche bei MusicBrainz zeigt nun auch das Album zum Suchbegriff an.

Das ist ein wichtiges Prinzip im Software-Design: Das Model bestimmt die einheitliche Sprache der App, nicht die API.

    Für den User ist es ein "Album".

    iTunes nennt es technisch collectionName.

    MusicBrainz nennt es technisch releases.

    Spotify nennt es wieder anders.

Die Aufgabe der Service-Dateien (musicbrainz.py, itunes.py) ist es, diese fremden Begriffe in die Sprache des Nutzers bzw. der App (album) zu übersetzen. Würde man stattdessen für jede API ein eigenes Feld einrichten (itunes_album, mb_release, spotify_context), würde das Model riesig und dein Code für die Anzeige (Formatter) ein Chaos aus if/else.




