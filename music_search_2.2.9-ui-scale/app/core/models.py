# core/models.py
from dataclasses import dataclass
from typing import Any, List # List explizit importieren für ältere Python Versionen
from enum import Enum, auto

@dataclass
class Track:
    title: str
    artist: str
    album: str | None  # Hier speichern wir ALLES (iTunes collection, MB releases)
    year: str | None   # <--- NEU: einheitlich mit Book 

@dataclass
class Book:
    title: str
    author: list
    year: str | None
    publisher: str | None
    isbn: str | None

@dataclass
class SearchResult:
    source: str 
    tracks: List[Any] # List explizit verwenden für ältere Python Versionen
    total: int

    def __post_init__(self):
        if not isinstance(self.tracks, list):
            raise TypeError("SearchResult.tracks must be a list")
 
class SearchDomain(Enum):
    ALL = auto()
    MUSIC = auto()
    LITERATURE = auto()
    CONTEXT = auto()

    def __str__(self):
        return self.name.lower()

# ----------------------------------------------------------
# Alte Version des Codes (auskommentiert)
# ----------------------------------------------------------


# from dataclasses import dataclass
# from typing import Any
# from enum import Enum, auto

# @dataclass
# class Track:
#     title: str
#     artist: str
#     album: str | None
#     #source: str  # "itunes"| "musicbrainz"

# @dataclass
# class Book:
#     title: str
#     author: list
#     year: str | None
#     publisher: str | None
#     isbn: str | None

# @dataclass
# class SearchResult:
#     source: str  # "itunes"| "musicbrainz" | "openlibrary"
#     #tracks: list[Track]
#     tracks: list[Any]
#     total: int

#     def __post_init__(self):
#         if not isinstance(self.tracks, list):
#             raise TypeError("SearchResult.tracks must be a list")
 
# class SearchDomain(Enum):
#     ALL = auto()
#     MUSIC = auto()
#     LITERATURE = auto()
#     CONTEXT = auto()

#     def __str__(self):
#         return self.name.lower()
