# app/core/formatters/styles.py
"""
Docstring for music_search_2.2.7
Formatters: Common CSS styles for HTML searchresults.
"""


def get_common_css(accent_color):
    return f"""
    <style>
        /* --- BILDSCHIRM --- */
        body {{
            font-family: 'Segoe UI', Verdana, sans-serif;
            color: #ffffff; /* Alles Weiß für maximalen Kontrast */
            background-color: transparent;
            margin: 8px;
        }}

        /* Überschrift */
        h2.main-title {{
            color: {accent_color}; 
            border-bottom: 3px solid {accent_color};
            margin-bottom: 25px;
            font-size: 1.6em;
        }}

        .results-meta {{
            color: #ffffff;
            font-weight: bold;
            margin-bottom: 20px;
        }}

        ul.result-list {{
            list-style-type: none; 
            padding: 0; margin: 0;
        }}

        li.result-item {{
            margin: 0; padding: 0;
        }}

        /* --- DATA BLOCKS --- */
        
        /* 1. Titel: Groß, Fett, KEIN Abstand nach unten */
        div.book-title {{
            font-size: 1.4em;
            font-weight: bold;
            color: #ffffff;
            margin-top: 0px;
            margin-bottom: 2px; /* Nur winziger Abstand zum Autor */
        }}
        
        /* 2. Autor: Groß, KEIN Abstand nach oben */
        div.author-info {{
            font-size: 1.2em;
            font-weight: normal;
            color: #ffffff; 
            margin-top: 0px;      /* Zieht es direkt an den Titel ran */
            margin-bottom: 8px;   /* Etwas Luft zu den Details */
        }}
        
        /* Label "Autor:" */
        span.label {{
            font-weight: bold;
            margin-right: 8px;
        }}

        /* 3. Details */
        div.meta-info {{
            font-size: 1.0em;
            color: #ffffff;
        }}

        span.meta-separator {{
            color: {accent_color};
            font-weight: bold;
            margin: 0 8px;
        }}

        /* --- DIE TRENNLINIE (HR) --- */
        /* Das ist der Abstandhalter zwischen den Büchern */
        hr.separator {{
            background-color: {accent_color}; /* Farbe der Linie */
            height: 3px;          /* Dicke der Linie */
            border: none;         /* Kein Standard-Rahmen */
            margin-top: 15px;     /* Abstand zum aktuellen Buch */
            margin-bottom: 25px;  /* Großer Abstand zum NÄCHSTEN Buch */
        }}


        /* --- DRUCK (Schwarz auf Weiß) --- */
        @media print {{
            body {{
                background-color: #ffffff !important;
                color: #000000 !important;
            }}
            div.book-title, div.author-info, div.meta-info {{
                color: #000000 !important;
            }}
            hr.separator {{
                background-color: #000000 !important;
                height: 1px;
            }}
            li.result-item {{
                page-break-inside: avoid;
            }}
        }}
    </style>
    """