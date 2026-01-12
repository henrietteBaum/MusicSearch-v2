# app/core/formatter/mb_formatter.py
"""
Returns a minimal, screenreader-friendly HTML representation
of MusicBrainz search results.
"""


def format_mb_results(tracks, total: int) -> str:
    lines = []

    # Header
    lines.append("<h2>MusicBrainz - Search Results </h2>")
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
