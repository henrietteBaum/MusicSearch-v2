from app.core.search import search_all

def run():
    term = input("Enter search term: ")
    results = search_all(term)

    for track in results:
        print(f"[{track.source}] {track.artist} - {track.title}")