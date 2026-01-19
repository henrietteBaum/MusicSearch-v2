# app/services/openlibrary.py

import requests
from core.models import Book, Track
from core.models import SearchResult

OPEN_LIBRARY_URL = "https://openlibrary.org/search.json"

BASE_PARAMS = {
    "q": "",                                
    "fields": "author_name,title,publisher,first_publish_year,isbn",
    "limit": 10,
    "lang": "de, en"
}

def search(term: str, limit: int = 5, mode: str = "all") -> SearchResult:
    
    params = BASE_PARAMS.copy()

    if mode == "artist":
        query_string = f'author:({term})'
    elif mode == "title":
        query_string = f'title:({term})'
    else:
        # Smart Search
        query_string = f'title:({term}) OR author:({term})'

    #query_string = f"title:({term}) OR author:({term})"
    
    params["q"] = query_string
    # params["q"] = term
    params["sort"] = "editions"
    params["limit"] = limit


    try:
        response = requests.get(OPEN_LIBRARY_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

    except (requests.RequestException, ValueError) as e:
        print(f"OpenLibrary API Fehler: {e}")
        return SearchResult(tracks=[], total=0, source="openlibrary")

    
    books = []

    for doc in data.get("docs", []):

        title = doc.get("title", "Titel unbekannt")

        # Autoren: Max 3 Autoren, sonst wird es zu lang zum Vorlesen
        authors_list = doc.get("author_name", [])
        if authors_list:
            author_str = ", ".join(authors_list[:3]) # Max 3 Autoren, sonst wird es zu lang zum Vorlesen
            if len(authors_list) > 3:
                author_str += " u.a."
        else:
            author_str = "Autor unknown"

        # Verlag: Nur den ersten nehmen, Listen sind oft vermüllt
        publisher_list = doc.get("publisher", [])
        if publisher_list:
            publisher_str = publisher_list[0]
        else:
            publisher_str = "No publisher info"

        # Jahr
        year_val = doc.get("first_publish_year")
        year_str = str(year_val) if year_val else "Year unknown"

        # ISBN
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

