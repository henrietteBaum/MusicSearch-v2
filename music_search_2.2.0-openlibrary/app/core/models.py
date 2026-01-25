from dataclasses import dataclass
from typing import Any

@dataclass
class Track:
    title: str
    artist: str
    album: str | None
    #source: str  # "itunes"| "musicbrainz"

@dataclass
class Book:
    title: str
    author: list
    year: str | None
    publisher: str | None

@dataclass
class SearchResult:
    source: str  # "itunes"| "musicbrainz" | "openlibrary"
    #tracks: list[Track]
    tracks: list[Any]
    total: int

    def __post_init__(self):
        if not isinstance(self.tracks, list):
            raise TypeError("SearchResult.tracks must be a list")
 

