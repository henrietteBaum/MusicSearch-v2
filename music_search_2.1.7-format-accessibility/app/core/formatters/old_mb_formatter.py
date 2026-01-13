# app/core/formatter/mb_formatter.py
"""
Returns a minimal, screenreader-friendly HTML representation
of MusicBrainz search results.
"""
from core.formatters.styles import get_common_css

def format_mb_results(tracks, total: int) -> str:
    lines = []

    # HTML Grundgerüst starten
    lines.append("<html><head>")
    lines.append(get_common_css())
    lines.append("</head><body>")

    # Header
    lines.append("<h2>MusicBrainz - Search Results </h2>")
    lines.append(
        f"<p class='results-meta'>Total results: {total} | Showing: {len(tracks)}</p>"
    )

    if not tracks:
        lines.append("<p>No results found</p>")
        lines.append("</body></html>")
        return "\n".join(lines)
    
    # Results
    for track in tracks:
        block = (
            "<li class='result-item'>"
            f"<div class='artist-title'>{track.artist} - {track.title}</div>"
            f"<div class='album-info'>Album: {track.album or '-'}</div>"
            "</li>"
        )

        # block = (
        #     "<p>"
        #     f"{track.artist} - {track.title}<br>"
        #     f"Album: {track.album or '-'}"
        #     "</p>"
        # )
        lines.append(block)

    lines.append("</ul>")
    lines.append("</body></html>")

    return "\n".join(lines)
