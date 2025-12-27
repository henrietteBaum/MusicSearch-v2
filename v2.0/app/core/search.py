from app.services import itunes, musicbrainz
from app.core.models import Track

def search_all(term: str) -> list[Track]:
    results: list[Track] = []

    results.extend(itunes.search(term))
    results.extend(musicbrainz.search(term))

    return results