# core/search.py

from services import itunes, musicbrainz, openlibrary
from core.models import SearchResult, SearchDomain

# app/core/search.py

from core.models import SearchDomain, SearchResult
# Importiere deine Services
from services import itunes, musicbrainz, openlibrary
import concurrent.futures

def search_all(term: str, limit: int, domain: SearchDomain, mode: str = "all") -> dict[str, SearchResult]:
    
    results = {}

    # Wir nutzen ThreadPoolExecutor für parallele Anfragen
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {}

        # --- iTunes ---
        # Sucht nur, wenn Domain ALL oder MUSIC ist
        if domain in (SearchDomain.ALL, SearchDomain.MUSIC):
            # Wir übergeben jetzt 'mode' an die itunes.search Funktion
            futures[executor.submit(itunes.search, term, limit, mode)] = "itunes"

        # --- MusicBrainz ---
        if domain in (SearchDomain.ALL, SearchDomain.MUSIC):
            futures[executor.submit(musicbrainz.search, term, limit, mode)] = "musicbrainz"

        # --- OpenLibrary ---
        if domain in (SearchDomain.ALL, SearchDomain.LITERATURE):
            futures[executor.submit(openlibrary.search, term, limit, mode)] = "openlibrary"

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


# -----# Deprecated: Use specific search functions instead----- #

# def search_all(term: str, limit: int = 10, domain: SearchDomain = SearchDomain.ALL) -> dict[str, SearchResult]:

#     results = {
#         "itunes": SearchResult(source="itunes", tracks=[], total=0),
#         "musicbrainz": SearchResult(source="musicbrainz", tracks=[], total=0),
#         "openlibrary": SearchResult(source="openlibrary", tracks=[], total=0)
#     }

#     # Music-Part
#     if domain == SearchDomain.ALL or domain == SearchDomain.MUSIC:
#         try:
#             results["itunes"] = itunes.search(term, limit)
#         except Exception as e:
#             print(f"DEBUG: iTunes Error: {e}")
            
#         try:
#             results["musicbrainz"] = musicbrainz.search(term, limit)
#         except Exception as e:
#             print(f"DEBUG: MB Error: {e}")

#     # Literature-Part
#     if domain == SearchDomain.ALL or domain == SearchDomain.LITERATURE:
#         try:
#             results["openlibrary"] = openlibrary.search(term, limit)
#         except Exception as e:
#             print(f"DEBUG: OpenLibrary Error: {e}")

#     return results
