import requests
from core.models import Track
from core.models import SearchResult

ITUNES_URL = "https://itunes.apple.com/search"

def search(term: str, limit: int = 5) -> SearchResult:
    params = {
        "term": term,
        "media": "music",
        "limit": limit
    }
    response = requests.get(ITUNES_URL, params=params)
    response.raise_for_status()

    data = response.json()
    tracks = []

    for item in data.get("results", []):
        tracks.append(
            Track(
                title=item.get("trackName"),
                artist=item.get("artistName"),
                album=item.get("collectionName"),
                #source="itunes"
            )
        )

    total_count = data.get("resultCount", 0)
    
    #return tracks, total_count

    return SearchResult(
        tracks=tracks,
        total=total_count,
        source="itunes"
    )