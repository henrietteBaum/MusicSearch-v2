from app.services import itunes, musicbrainz
from app.core.models import Track

def search_all(term: str) -> tuple[list[Track], int, int]:
    
    # tracks: list[Track] = []

    # tracks.extend(itunes.search(term))
    # tracks.extend(musicbrainz.search(term))

    # return tracks

    itunes_tacks, itunes_total = itunes.search(term)
    mb_tracks, mb_total = musicbrainz.search(term)

    tracks = itunes_tacks + mb_tracks
    
    return tracks, itunes_total, mb_total