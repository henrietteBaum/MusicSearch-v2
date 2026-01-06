from services import itunes, musicbrainz
from core.models import SearchResult

def search_all(term: str, limit: int = 10) -> dict[str, SearchResult]:
    
    # tracks: list[Track] = []
    # tracks.extend(itunes.search(term))
    # tracks.extend(musicbrainz.search(term))
    # return tracks

    itunes_tracks, itunes_total = itunes.search(term, limit)
    mb_tracks, mb_total = musicbrainz.search(term, limit)

    return {
        "itunes": SearchResult(
            source="itunes",
            tracks=itunes_tracks,
            total=itunes_total,
        ),
        "musicbrainz": SearchResult(
            source="musicbrainz",
            tracks=mb_tracks,
            total=mb_total,
        ),
    }