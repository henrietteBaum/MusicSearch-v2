# core/search.py

from core.models import SearchDomain, SearchResult
from services import itunes, musicbrainz, openlibrary, corelib
import concurrent.futures

def search_all(term: str, limit: int, domain: SearchDomain, mode: str = "all") -> dict[str, SearchResult]:
    
    results = {}

    # Wir nutzen ThreadPoolExecutor für parallele Anfragen
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {}

        # --- iTunes ---
        # Sucht nur, wenn Domain ALL oder MUSIC ist
        if domain in (SearchDomain.ALL, SearchDomain.MUSIC):
            # 'mode' an die itunes.search Funktion
            futures[executor.submit(itunes.search, term, limit, mode)] = "itunes"

        # --- MusicBrainz ---
        if domain in (SearchDomain.ALL, SearchDomain.MUSIC):
            futures[executor.submit(musicbrainz.search, term, limit, mode)] = "musicbrainz"

        # --- OpenLibrary ---
        if domain in (SearchDomain.ALL, SearchDomain.LITERATURE):
            futures[executor.submit(openlibrary.search, term, limit, mode)] = "openlibrary"

        # --- CORE ---
        if domain in (SearchDomain.ALL, SearchDomain.CONTEXT):
            futures[executor.submit(corelib.search, term, limit, mode)] = "core"

        # Ergebnisse einsammeln
        for future in concurrent.futures.as_completed(futures):
            source_name = futures[future]
            try:
                data = future.result()
                results[source_name] = data
            except Exception as e:
                print(f"Error searching {source_name}: {e}")
                # Leeres Ergebnis bei Fehler, um Absturz zu verhindern
                results[source_name] = SearchResult(source=source_name, tracks=[], total=0)

    return results


