# app/services/openlibrary.py

import requests
from core.models import Book, Track
from core.models import SearchResult

OPEN_LIBRARY_URL = "https://openlibrary.org/search.json"

SEARCH_PARAMS = {
    "q": "",                                
    "fields": "author_name,title,publisher,first_publish_year,isbn",
    "limit": 10                             
}

def search(term: str, limit: int = 5):

    # params = {
    #     "q": term,
    #     "limit": limit,
    #     "fields": "title,author_name,first_publish_year,publisher"
    # }
    params = SEARCH_PARAMS.copy()
    params["q"] = term
    params["limit"] = limit


    try:
        response = requests.get(OPEN_LIBRARY_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
    except (requests.RequestException, ValueError) as e:
        print(f"Fehler bei der Anfrage: {e}")
        return SearchResult(tracks=[], total=0, source="openlibrary")
    
    books = []

    for doc in data.get("docs", []):
        #year_val = doc.get("first_publish_year")
        #year_str = str(year_val) if year_val else "-"

        books.append(
            Book(
                title=doc.get("title"),
                author=", ".join(doc.get("author_name", [])),
                year=doc.get("first_publish_year"),
                publisher=", ".join(doc.get("publisher", ["-"])[:2])  # only the 2 first
            )
        )

        
    total_count = data.get("numFound", 0)

    return SearchResult(
        tracks=books,
        total=total_count,
        source="openlibrary"
    )

