# app/core/formatters/core_formatter.py

from core.formatters.styles import get_common_css

def format_core_results(books, total: int, accent_color) -> str:
    style = get_common_css(accent_color)
    
    html = [
        "<html><head>", style, "</head><body>",
        "<h2 class='main-title'>Scientific Context (CORE)</h2>",
        f"<p class='results-meta'>Found: {total} | Showing: {len(books)}</p>",
        "<ul class='result-list'>"
    ]

    for book in books:
        # Autoren
        if isinstance(book.author, list):
            authors_str = ", ".join(book.author)
        else:
            authors_str = str(book.author or "Unknown")

        html.append(f"""
            <li class="result-item">
                <div class="book-title">{book.title}</div>
                
                <div class="author-info">
                    <span class="label">Authors:</span>{authors_str}
                </div>
                
                <div class="meta-info">
                    {book.year or "-"} 
                    <span class='meta-separator'>|</span> 
                    {book.publisher}
                </div>
                
                <hr class="separator">
            </li>
        """)

    html.append("</ul></body></html>")
    return "".join(html)