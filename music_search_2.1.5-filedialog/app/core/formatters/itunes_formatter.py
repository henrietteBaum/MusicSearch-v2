# app/core/formatter/itunes_formatter.py
"""
Returns a minimal, screenreader-friendly HTML representation
of iTunes search results.
"""


def format_itunes_results(tracks, total: int) -> str:
    lines = []

    # Header
    lines.append("<h2>iTunes - Search Results </h2>")
    lines.append(
        f"<p>Total results: {total} | Showing: {len(tracks)}</p>"
    )

    if not tracks:
        lines.append("<p>No results found</p>")
        return "\n".join(lines)
    
    # Results
    for track in tracks:
        block = (
            "<p>"
            f"{track.artist} - {track.title}<br>"
            f"Album: {track.album or '-'}"
            "</p>"
        )
        lines.append(block)

    return "\n".join(lines)
