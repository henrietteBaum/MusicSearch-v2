from services import itunes, musicbrainz, openlibrary
from core.models import SearchResult, SearchDomain

# core/search.py

def search_all(term: str, limit: int = 10, domain: SearchDomain = SearchDomain.ALL) -> dict[str, SearchResult]:

    results = {
        "itunes": SearchResult(source="itunes", tracks=[], total=0),
        "musicbrainz": SearchResult(source="musicbrainz", tracks=[], total=0),
        "openlibrary": SearchResult(source="openlibrary", tracks=[], total=0)
    }

    # Music-Part
    if domain == SearchDomain.ALL or domain == SearchDomain.MUSIC:
        try:
            results["itunes"] = itunes.search(term, limit)
        except Exception as e:
            print(f"DEBUG: iTunes Error: {e}")
            
        try:
            results["musicbrainz"] = musicbrainz.search(term, limit)
        except Exception as e:
            print(f"DEBUG: MB Error: {e}")

    # Literature-Part
    if domain == SearchDomain.ALL or domain == SearchDomain.LITERATURE:
        try:
            results["openlibrary"] = openlibrary.search(term, limit)
        except Exception as e:
            print(f"DEBUG: OpenLibrary Error: {e}")

    return results
