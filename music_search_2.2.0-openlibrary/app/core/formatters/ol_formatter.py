# app/core/formatter/ol_formatter.py

from core.formatters.styles import get_common_css


def format_ol_results(books, total: int) -> str:
    style = get_common_css()
    html = [
        "<html><head>", style, "</head><body>",
        "<h2>OpenLibrary - Search Results</h2>",
        f"<p class='results-meta'>Total: {total} | Showing: {len(books)}</p>",
        "<ul style='list-style-type: none; padding: 0;'>"
    ]

    for book in books:
        html.append(f"""
            <li class="result-item">
                <div class="artist-title">
                    {book.author} - {book.title}
                </div>
                <div class="album-info">
                    First published: {book.year or "-"} | 
                    Publisher: {book.publisher or "-"}
                </div>
            </li>
        """)

    html.append("</ul></body></html>")
    return "".join(html)