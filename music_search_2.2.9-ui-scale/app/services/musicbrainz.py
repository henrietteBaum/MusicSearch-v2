import requests
from typing import List, Tuple
from core.models import Track
from core.models import SearchResult

MB_URL = "https://musicbrainz.org/ws/2/recording"

HEADER = {
    "User-Agent": "MusicSearchLearningApp/2.0 (info@computer-und-sehen.de)"
}

def search(term: str, limit: int = 5, mode: str = "all") ->  SearchResult:   #tuple[list[Track], int]:

    """
    Sucht in MusicBrainz.
    mode: 'all', 'artist', 'title', 'album'
    """
    # Anführungszeichen entfernen, um Syntaxfehler zu vermeiden
    clean_term = term.replace('"', '')

    # --- FILTER LOGIK ---
    # Hier entscheiden wir, wie gesucht wird
    
    if mode == "artist":
        # Strikte Suche: Der Begriff MUSS im Künstler-Feld stehen
        query_string = f'artist:"{clean_term}"'
        
    elif mode == "title":
        # Strikte Suche: Der Begriff MUSS im Titel (recording) stehen
        query_string = f'recording:"{clean_term}"'
        
    elif mode == "album":
        # Strikte Suche: Der Begriff MUSS im Album (release) stehen
        query_string = f'release:"{clean_term}"'
        
    else:
        # Fallback "all" (Smart Search)
        # Wir suchen überall, geben aber dem Künstler einen Boost (^3)
        # Das bedeutet: Treffer beim Künstler zählen 3x so viel wie im Titel.
        query_string = (
            f'artist:"{clean_term}"^3 OR '
            f'release:"{clean_term}"^2 OR '
            f'recording:"{clean_term}"'
        )


    params = {
        "query": query_string,
        "fmt": "json",
        "limit": limit
    }
    try:
        response = requests.get(MB_URL, params=params, headers=HEADER)
        response.raise_for_status()

        data = response.json()
        recordings = data.get("recordings", [])
        tracks: List[Track] = []


        for item in recordings:
            
            # 1. Artist (bleibt gleich)
            credits = item.get("artist-credit", [])
            if credits:
                artist_str = "".join([f"{c.get('name', '')}{c.get('joinphrase', '')}" for c in credits])
            else:
                artist_str = "Unknown Artist"

            # 2. Album & Jahr (OPTIMIERT)
            releases = item.get("releases", [])
            
            best_album_name = "-"
            best_year_str = "-"
            
            # Startwerte für die Suche nach dem besten Release
            oldest_date = "9999" 
            found_official = False # Haben wir schon ein "Official" Release gefunden?

            for rel in releases:
                title = rel.get("title", "-")
                date = rel.get("date", "")      # z.B. "1975-03-07"
                status = rel.get("status", "")  # z.B. "Official", "Bootleg", "Promotion"
                
                # Wir extrahieren nur das Jahr (ersten 4 Zeichen)
                year = date[:4] if date else ""

                # LOGIK:
                # Wir wollen ein Release mit Jahr.
                if year:
                    # Ist das aktuelle Release "Official"?
                    is_current_official = (status == "Official")
                    
                    # Entscheidungsbaum:
                    
                    # Fall A: Wir haben noch gar kein Jahr gefunden -> Nimm dieses
                    if best_year_str == "-":
                        best_year_str = year
                        best_album_name = title
                        oldest_date = year
                        found_official = is_current_official

                    # Fall B: Wir haben schon eins, aber das neue ist "Official" und das alte war es nicht?
                    # -> Nimm das neue, auch wenn es vielleicht jünger ist (lieber offiziell als Bootleg)
                    elif is_current_official and not found_official:
                        best_year_str = year
                        best_album_name = title
                        oldest_date = year
                        found_official = True
                    
                    # Fall C: Gleicher Status (beide Official oder beide nicht), aber das neue ist ÄLTER?
                    # -> Nimm das ältere.
                    elif is_current_official == found_official:
                        if year < oldest_date:
                            best_year_str = year
                            best_album_name = title
                            oldest_date = year

            # Fallback: Wenn gar keine Releases mit Datum da waren, nimm einfach den Titel des ersten
            if best_album_name == "-" and releases:
                best_album_name = releases[0].get("title", "-")

            tracks.append(
                Track(
                    title=item.get("title", "Unknown Title"),
                    artist=artist_str,
                    album=best_album_name,
                    year=best_year_str
                )
            )

        # Sortierung: Aufsteigend nach Jahr.
        # Einträge ohne Jahr ("-") kommen ans Ende ("9999").
        tracks.sort(key=lambda t: t.year if t.year != "-" else "9999")

        total_count = data.get("count", 0)

    except Exception as e:
        print(f"DEBUG MusicBrainz: API not requested, {e}")
        return SearchResult(tracks=[], total=0, source="musicbrainz")

    return SearchResult(
        tracks=tracks,
        total=total_count,
        source="musicbrainz"
    )
        


        # ------

        # for item in recordings:

        #     # 1. Artist mapping (wie vorher besprochen)
        #     credits = item.get("artist-credit", [])
        #     if credits:
        #         artist_str = "".join([f"{c.get('name', '')}{c.get('joinphrase', '')}" for c in credits])
        #     else:
        #         artist_str = "Unknown Artist"

        #     # 2. Album & Jahr mapping (DAS IST NEU)
        #     releases = item.get("releases", [])
        #     album_name = "-"
        #     year_str = "-"


        #      # --- VERBESSERTE LOGIK: Ältestes Release finden ---
        #     releases = item.get("releases", [])
            
        #     best_album_name = "-"
        #     best_year_str = "-"
            
        #     # Wir setzen ein extrem hohes Start-Datum zum Vergleichen
        #     oldest_date = "9999-99-99" 
        #     found_valid_release = False

        #     for rel in releases:
        #         # Datum holen (kann "1983-04-14", "1983" oder leer sein)
        #         rel_date = rel.get("date", "")
                
        #         # Wir brauchen mindestens ein Datum, um zu vergleichen
        #         if rel_date and rel_date < oldest_date:
        #             oldest_date = rel_date
        #             best_album_name = rel.get("title", "-")
        #             best_year_str = rel_date[:4] # Nur das Jahr
        #             found_valid_release = True
            
        #     # Fallback: Wenn gar kein Release ein Datum hatte, nehmen wir einfach das erste (falls vorhanden)
        #     if not found_valid_release and releases:
        #         best_album_name = releases[0].get("title", "-")


        #     tracks.append(
        #         Track(
        #             title=item.get("title", "Unknown Title"),
        #             artist=artist_str,
        #             album=best_album_name, # Jetzt das Album der ältesten Veröffentlichung
        #             year=best_year_str     # Jetzt das Jahr der ältesten Veröffentlichung
        #         )
        #     )


            # ----- ALTE LOGIK: Erstes Release nehmen ----- 

            # if releases:
            #     # Wir nehmen einfach das erste Release als "Album"
            #     first_release = releases[0]
            #     album_name = first_release.get("title", "-")
                
            #     # Datum versuchen zu finden (Format ist oft YYYY-MM-DD oder YYYY)
            #     date = first_release.get("date", "")
            #     if date:
            #         year_str = date[:4] # Wir nehmen nur die ersten 4 Zeichen (das Jahr)

            # tracks.append(
            #     Track(
            #         title=item.get("title", "Unknown Title"),
            #         artist=artist_str,
            #         album=album_name, # Hier mappen wir 'release' auf 'album'
            #         year=year_str     # <--- Das neue Feld
            #     )
            # )


    #     total_count = data.get("count", 0)
    #     #return tracks, total_count

    # except Exception as e:
    #     print(f"DEBUG MusicBrainz: API not requested, {e}")
    #     return SearchResult(tracks=[], total=0, source="musicbrainz")
    

    # OPTIONAL: Chronologische Sortierung der gefundenen Treffer
    # Wir sortieren die Liste 'tracks' nach Jahr. 
    # Wenn kein Jahr da ist ("-"), kommt es ans Ende ("9999").
    # tracks.sort(key=lambda t: t.year if t.year != "-" else "9999")

    # return SearchResult(
    #     tracks=tracks,
    #     total=total_count,
    #     source="musicbrainz"
    # )