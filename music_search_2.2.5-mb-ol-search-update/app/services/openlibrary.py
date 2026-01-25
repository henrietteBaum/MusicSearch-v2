# app/services/openlibrary.py

import requests
from core.models import Book, SearchResult

OPEN_LIBRARY_URL = "https://openlibrary.org/search.json"

BASE_PARAMS = {
    "fields": "author_name,title,publisher,first_publish_year,isbn",
    "limit": 10,
    "lang": "de,en"
}

def search(term: str, limit: int = 5, mode: str = "all") -> SearchResult:
    # Kopie der Basis-Parameter erstellen
    params = BASE_PARAMS.copy()
    params["limit"] = limit

    # Wir nutzen nun spezifische Parameter statt der "q"-Syntax
    # Das filtert wesentlich präziser!
    if mode == "artist":
        params["author"] = term
    elif mode == "title":
        params["title"] = term
    else:
        # Falls "all" oder unbekannt, nutzen wir 'q' als Fallback
        # Wir entfernen aber das 'sort=editions', da es oft irrelevante 
        # Bestseller (wie Alice) nach oben schiebt.
        params["q"] = term

    try:
        # Timeout ist wichtig für die Barrierefreiheit, damit die App nicht einfriert
        response = requests.get(OPEN_LIBRARY_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

    except (requests.RequestException, ValueError) as e:
        print(f"OpenLibrary API Fehler: {e}")
        return SearchResult(tracks=[], total=0, source="openlibrary")

    books = []
    
    # Optionaler "Härtefilter" für die Titelsuche:
    # Wir prüfen im Code noch einmal nach, ob der Begriff wirklich im Titel steht.
    docs = data.get("docs", [])
    
    for doc in docs:
        title = doc.get("title", "Titel unbekannt")
        
        # Wenn der User spezifisch nach Titeln sucht, filtern wir "Rauschen" aus
        if mode == "title" and term.lower() not in title.lower():
            continue

        # Autoren-Verarbeitung (optimiert für Screenreader)
        authors_list = doc.get("author_name", [])
        if authors_list:
            author_str = ", ".join(authors_list[:3])
            if len(authors_list) > 3:
                author_str += " u.a."
        else:
            author_str = "Autor unbekannt"

        # Verlag-Verarbeitung
        publisher_list = doc.get("publisher", [])
        publisher_str = publisher_list[0] if publisher_list else "Keine Verlagsangabe"

        # Jahr & ISBN
        year_val = doc.get("first_publish_year")
        year_str = str(year_val) if year_val else "Jahr unbekannt"
        
        isbn_list = doc.get("isbn", [])
        isbn_val = isbn_list[0] if isbn_list else None
        
        books.append(
            Book(
                title=title,
                author=author_str,
                year=year_str,
                publisher=publisher_str,
                isbn=isbn_val
            )
        )

    total_count = data.get("numFound", 0)

    return SearchResult(
        tracks=books,
        total=total_count,
        source="openlibrary"
    )