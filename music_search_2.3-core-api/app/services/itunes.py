import requests
from core.models import Track
from core.models import SearchResult

ITUNES_URL = "https://itunes.apple.com/search"


def search(term: str, limit: int = 5, mode: str="all") -> SearchResult:

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

        # iTunes liefert "2005-03-01T12:00:00Z"
        raw_date = item.get("releaseDate", "")
        year_str = raw_date[:4] if raw_date else "-"

        tracks.append(
            Track(
                title=item.get("trackName"),
                artist=item.get("artistName"),
                album=item.get("collectionName"), # iTunes nennt es collectionName -> wir mappen auf album
                year=year_str
            )
        )


    # Alle verfügbaren Tracks zählen
    total_count = data.get("resultCount", 0)
    

    return SearchResult(
        tracks=tracks,
        total=total_count,
        source="itunes"
    )