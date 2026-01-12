import requests
from typing import List, Tuple
from core.models import Track

MB_URL = "https://musicbrainz.org/ws/2/recording"

HEADER = {
    "User-Agent": "MusicSearchLearningApp/2.0 (info@computer-und-sehen.de)"
}

def search(term: str, limit: int = 5) -> tuple[list[Track], int]:
    params = {
        "query": term,
        "fmt": "json",
        "limit": limit
    }
    response = requests.get(MB_URL, params=params, headers=HEADER)
    response.raise_for_status()

    data = response.json()
    recorcings = data.get("recordings", [])
    tracks: List[Track] = []

    for item in recorcings:
        artist = item["artist-credit"][0]["name"] if item.get("artist-credit") else "Unknown"
        tracks.append(
            Track(
                title=item.get("title"),
                artist=artist,
                album=None,
                #source="musicbrainz"
            )
        )

    total_count = data.get("count", 0)
    return tracks, total_count