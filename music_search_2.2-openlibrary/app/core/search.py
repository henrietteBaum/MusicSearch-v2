from services import itunes, musicbrainz, openlibrary
from core.models import SearchResult

def search_all(term: str, limit: int = 10) -> dict[str, SearchResult]:
    
    return {
        "itunes": itunes.search(term, limit),
        "musicbrainz": musicbrainz.search(term, limit),
        "openlibrary": openlibrary.search(term, limit)
    }