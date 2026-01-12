from dataclasses import dataclass

@dataclass
class Track:
    title: str
    artist: str
    album: str | None
    #source: str  # "itunes"| "musicbrainz"

@dataclass
class SearchResult:
    source: str  # "itunes"| "musicbrainz"
    tracks: list[Track]
    total: int
 