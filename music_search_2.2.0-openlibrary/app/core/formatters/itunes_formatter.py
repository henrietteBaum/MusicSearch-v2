# app/core/formatter/itunes_formatter.py
"""
Returns a minimal, screenreader-friendly HTML representation
of iTunes search results.
"""
from core.formatters.styles import get_common_css

def format_itunes_results(tracks, total: int) -> str:
    style = get_common_css()
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        {style}
    </head>
    <body>
        <h2>iTunes - Search Results</h2>
        <p class="results-meta">Total results: {total} | Showing: {len(tracks)}</p>
        <ul style="list-style-type: none; padding: 0;">
    """

    for track in tracks:
        html += f"""
            <li class="result-item">
                <div class="artist-title">{track.artist} - {track.title}</div>
                <div class="album-info">Album: {track.album or '-'}</div>
            </li>
        """

    html += """
        </ul>
    </body>
    </html>
    """
    return html