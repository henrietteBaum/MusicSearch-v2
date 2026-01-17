# app/core/formatter/styles.py

# def get_common_css():
#     return """
#     <style>
#         /* Basis-Layout */
#         body { 
#             font-family: sans-serif; 
#             line-height: 1.6; 
#             margin: 20px; 
#         }

#         h2 { 
#             color: #3498db; 
#             border-bottom: 2px solid #3498db; 
#             padding-bottom: 5px; 
#             margin-top: 0;
#         }

#         /* Metadaten: Kein Kursiv, dafür mehr Abstand für bessere Lesbarkeit */
#         .results-meta { 
#             color: #666; 
#             letter-spacing: 0.05em; 
#             text-transform: uppercase; 
#             font-size: 0.9em;
#             margin-bottom: 20px; 
#         }

#         .result-item { 
#             margin-bottom: 15px; 
#             padding: 12px; 
#             border-left: 5px solid #3498db;
#             background-color: rgba(128, 128, 128, 0.1); 
#             border-radius: 0 4px 4px 0;
#         }

#         .artist-title { 
#             font-weight: bold; 
#             font-size: 1.15em; 
#             margin-bottom: 4px;
#         }

#         /* Album-Info: Kräftigeres Grau für besseren Kontrast am Bildschirm */
#         .album-info { 
#             color: #cccccc; 
#         }

#         /* SPEZIELLE ANPASSUNGEN FÜR DRUCK & PDF */
#         @media print {
#             body { 
#                 background-color: white !important; 
#                 color: black !important; 
#                 margin: 0; 
#                 font-size: 11pt; 
#             }
            
#             h2 { 
#                 color: #000 !important; 
#                 border-bottom: 1px solid #000; 
#             }
            
#             /* In der PDF/Druck alles in echtem Schwarz für maximale Lesbarkeit */
#             .results-meta, .artist-title, .album-info { 
#                 color: black !important; 
#             }
            
#             .result-item { 
#                 border: 1px solid #000; 
#                 background-color: transparent !important;
#                 page-break-inside: avoid; 
#             }
#         }
#     </style>
#     """

# app/core/formatters/styles.py

def get_common_css(accent_color): # Dein KDE-Blau
    return f"""
    <style>
        body {{
            font-family: sans-serif;
            line-height: 1.4;
            color: #efefef; /* Heller Text für Darkmode */
            background-color: transparent;
            margin: 10px;
        }}
        h2 {{
            color: {accent_color};
            border-bottom: 2px solid {accent_color};
            padding-bottom: 5px;
            font-size: 1.5em;
        }}
        .results-meta {{
            # font-style: italic;
            color: #888;
            margin-bottom: 20px;
            font-size: 0.9em;
        }}
        .result-item {{
            background-color: rgba(255, 255, 255, 0.03);
            border-left: 4px solid {accent_color};
            margin-bottom: 12px;
            padding: 10px 15px;
            border-radius: 2px;
        }}
        .artist-title {{
            font-weight: bold;
            font-size: 1.1em;
            color: #ffffff;
        }}
        .album-info {{
            color: #bbb;
            font-size: 0.95em;
            margin-top: 4px;
        }}
        /* Hover-Effekt für bessere Orientierung */
        li .result-item:hover {{
            background-color: rgba(255, 255, 255, 0.08);
        }}
        hr {{
            border: none;
            height: 1px;
            width: 100%;
            background-color: {accent_color};
            margin: 10px 0;
        }}
    </style>
    """