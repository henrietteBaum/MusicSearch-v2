"""
Docstring for app.ui.cli
Command-line interface for searching tracks across multiple sources.
Only used for Version 2.0 to show the basics, 2.1 uses a Qt-based GUI in file main_window.py. 
"""

from app.core.search import search_all

def run():
    term = input("Enter search term: ")
    results = search_all(term)

    for track in results:
        print(f"[{track.source}] {track.artist} - {track.title}")