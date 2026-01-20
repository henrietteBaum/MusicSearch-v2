# app/core/formatter/mb_formatter.py

from core.formatters.styles import get_common_css

def format_mb_results(tracks, total: int, accent_color) -> str:
    style = get_common_css(accent_color)
    
    html = [
        "<html><head>", style, "</head><body>",
        "<h2 class='main-title'>MusicBrainz Results</h2>",
        f"<p class='results-meta'>Found: {total} | Showing: {len(tracks)}</p>",
        "<ul class='result-list'>"
    ]

    for track in tracks:
        # Jahr-Anzeige vorbereiten
        # Nur wenn ein Jahr da ist, bauen wir den String inkl. Trenner (|)
        year_html = ""
        if track.year and track.year != "-":
            year_html = f"{track.year} <span class='meta-separator'>|</span> "


        # HTML bauen
        html.append(f"""
            <li class="result-item">
                <div class="book-title">{track.title}</div>
                
                <div class="author-info">
                    <span class="label">Artist: </span>{track.artist}
                </div>
                
                <div class="meta-info">
                    {year_html}
                    <span class="label">Album:</span> {track.album or '-'}
                </div>
               
                <hr class="separator">
            </li>
        """)

    # ----- Deprecated: Previous version without year -----
    # for track in tracks:
    #     html.append(f"""
    #         <li class="result-item">
    #             <div class="book-title">{track.title}</div>
                
    #             <div class="author-info">
    #                 <span class="label">Artist: </span>{track.artist}
    #             </div>
                
    #             <div class="meta-info">
    #                 <span class="label">Album: </span>{track.album or '-'}
    #             </div>
                
    #             <hr class="separator">
    #         </li>
    #     """)

    html.append("</ul></body></html>")
    return "".join(html)