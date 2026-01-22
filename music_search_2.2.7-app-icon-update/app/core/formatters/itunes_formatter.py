# app/core/formatter/itunes_formatter.py

from core.formatters.styles import get_common_css

def format_itunes_results(tracks, total: int, accent_color) -> str:
    style = get_common_css(accent_color)
    
    # Nutzung einer Liste für effizienteren String-Aufbau
    html = [
        "<html><head>", style, "</head><body>",
        "<h2 class='main-title'>iTunes Results</h2>",
        f"<p class='results-meta'>Found: {total} | Showing: {len(tracks)}</p>",
        "<ul class='result-list'>"
    ]

    for track in tracks:
        # Struktur identisch zu OpenLibrary:
        # 1. Zeile: Titel
        # 2. Zeile: Interpret (Artist)
        # 3. Zeile: Album
        
        html.append(f"""
            <li class="result-item">
                <div class="book-title">{track.title}</div>
                
                <div class="author-info">
                    <span class="label">Artist: </span>{track.artist}
                </div>
                
                <div class="meta-info">
                    <span class="label">Album: </span>{track.album or '-'}
                </div>
                
                <hr class="separator">
            </li>
        """)

    html.append("</ul></body></html>")
    return "".join(html)