# app/core/formatter/ol_formatter.py

from core.formatters.styles import get_common_css

def format_ol_results(books, total: int, accent_color) -> str:
    style = get_common_css(accent_color)
    
    html = [
        "<html><head>", style, "</head><body>",
        f"<h2 class='main-title'>OpenLibrary Results</h2>",
        f"<p class='results-meta'>Found: {total} | Showing: {len(books)}</p>",
        "<ul class='result-list'>"
    ]

    for book in books:
        # Autoren formatieren
        if isinstance(book.author, list):
            authors_str = ", ".join(book.author)
        else:
            authors_str = str(book.author or "Unknown")

        # ISBN Block vorbereiten
        isbn_html = ""
        if book.isbn:
            # Der Strich davor (|) bekommt die Akzentfarbe via CSS .meta-separator
            isbn_html = f"<span class='meta-separator'>|</span> ISBN: {book.isbn}"

        # HTML bauen
        # Struktur:
        # LI (Container)
        #   -> Titel (Groß, Fett)
        #   -> Autor (Groß, Weiß)
        #   -> Info (Normal, Weiß: Jahr | Verlag | ISBN)
        
        html.append(f"""

            <li class="result-item">
                <div class="book-title">{book.title}</div>
                
                <div class="author-info">
                    <span class="label">Autor: </span>{authors_str}
                </div>
                
                <div class="meta-info">
                    {book.year or "-"} 
                    <span class='meta-separator'>|</span> 
                    {book.publisher or "-"}
                    {isbn_html}
                </div>
                
                <hr class="separator">
            </li>
        """)

    html.append("</ul></body></html>")
    return "".join(html)