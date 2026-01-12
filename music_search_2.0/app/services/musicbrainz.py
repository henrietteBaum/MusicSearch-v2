import requests
from app.core.models import Track

MB_URL = "https://musicbrainz.org/ws/2/recording"

HEADER = {
    "User-Agent": "MusicSearchLearningApp/2.0 (info@computer-und-sehen.de)"
}

def search(term: str, limit: int = 5) -> list[Track]:
    params = {
        "query": term,
        "fmt": "json",
        "limit": limit
    }
    response = requests.get(MB_URL, params=params, headers=HEADER)
    response.raise_for_status()

    data = response.json()
    tracks = []

    for item in data.get("recordings", []):
        artist = item["artist-credit"][0]["name"] if item.get("artist-credit") else "Unknown"

        tracks.append(
            Track(
                title=item.get("title"),
                artist=artist,
                album=None,
                source="musicbrainz"
            )
        )
    
    return tracks