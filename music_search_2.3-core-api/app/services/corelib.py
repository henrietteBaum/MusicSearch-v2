# app/services/corelib.py

import requests
import keyring
from PySide6.QtWidgets import QInputDialog, QLineEdit 
from core.models import Book, SearchResult

APP_NAME = "MusicSearch2"
KEY_NAME = "api_key"
CORE_API_URL = "https://api.core.ac.uk/v3/search/works"


# ----- API-key Abfrage und Prüfung -----

def is_valid_key_format(key: str) -> bool:
    """
    Prüft, ob der Key technisch plausibel ist.
    Ein API-Key darf keine Zeilenumbrüche haben und ist meistens nicht riesig.
    """
    if not key:
        return False
    # Ein Key mit Zeilenumbrüchen ist definitiv falsch (z.B. versehentlich Code kopiert)
    if '\n' in key or '\r' in key:
        return False
    # CORE Keys sind alphanumerisch. Wenn er Leerzeichen enthält, ist er verdächtig.
    if ' ' in key:
        return False
    return True

def get_stored_key():
    """Holt den Key und prüft ihn auf Plausibilität."""
    try:
        key = keyring.get_password(APP_NAME, KEY_NAME)
        
        if key and not is_valid_key_format(key):
            print("DEBUG CORE: Gespeicherter Key ist fehlerhaft (sieht aus wie Code). Lösche ihn...")
            try:
                keyring.delete_password(APP_NAME, KEY_NAME)
            except:
                pass # Falls er schon weg ist
            return None
            
        return key
    except Exception as e:
        print(f"DEBUG CORE: Keyring Fehler: {e}")
        return None

def ensure_api_key(parent_window) -> bool:
    """
    Fragt den User interaktiv nach dem Key, falls noch keiner da ist.
    Muss im MAIN-THREAD aufgerufen werden!
    """
    # Erst prüfen, ob wir schon einen GÜLTIGEN Key haben
    if get_stored_key():
        return True
        
    # Dialog zeigen
    key, ok = QInputDialog.getText(
        parent_window, 
        "CORE API Key Required", 
        "Please enter your CORE API Key:\n(Free at https://core.ac.uk/services/api)",
        echo=QLineEdit.EchoMode.Password
    )
    
    if ok and key:
        # Bereinigen
        clean_key = key.strip()
        
        # Validieren bevor wir speichern
        if not is_valid_key_format(clean_key):
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(parent_window, "Invalid Key", "The text you entered does not look like an API key (it contains spaces or newlines). Please try again.")
            return False

        keyring.set_password(APP_NAME, KEY_NAME, clean_key)
        return True
    
    return False




# ----- API-key abfragen -----
# def has_api_key() -> bool:
#     """Prüft schnell, ob ein Key existiert, ohne zu fragen."""
#     return keyring.get_password(APP_NAME, KEY_NAME) is not None

# def ensure_api_key(parent_window) -> bool:
#     """
#     Fragt den User interaktiv nach dem Key, falls noch keiner da ist.
#     Muss im MAIN-THREAD aufgerufen werden!
#     """
#     if has_api_key():
#         return True
        
#     # Hier war der Fehler: QLineEdit.EchoMode.Password nutzen
#     key, ok = QInputDialog.getText(
#         parent_window, 
#         "CORE API Key Required", 
#         "Please enter your CORE API Key:\n(Free at https://core.ac.uk/services/api)",
#         echo=QLineEdit.EchoMode.Password # <--- KORREKTUR HIER
#     )
    
#     if ok and key:
#         keyring.set_password(APP_NAME, KEY_NAME, key.strip())
#         return True
    
#     return False

# def get_stored_key():
#     return keyring.get_password(APP_NAME, KEY_NAME)





def search(term: str, limit: int = 5, mode: str = "all") -> SearchResult:
    """
    Sucht nach wissenschaftlichen Artikeln in CORE.
    Nutzt das Book-Model (passt gut für Papers).
    """
    api_key = get_stored_key()
    
    if not api_key:
        # Kein Key -> Leeres Ergebnis (oder Fehlerbehandlung)
        print("DEBUG CORE: Kein API Key vorhanden.")
        return SearchResult(tracks=[], total=0, source="core")

    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    # Suchanfrage bauen
    # CORE unterstützt einfache Queries. Wir geben den Term weiter.
    params = {
        "q": term,
        "limit": limit
    }

    try:
        response = requests.get(CORE_API_URL, params=params, headers=headers, timeout=10)
        
        if response.status_code in (401, 403):
            print("DEBUG CORE: API Key ungültig oder abgelaufen.")
            # Optional: Key aus Keyring löschen, damit beim nächsten Mal neu gefragt wird
            # keyring.delete_password(APP_NAME, KEY_NAME)
            return SearchResult(tracks=[], total=0, source="core")
            
        response.raise_for_status()
        data = response.json()
        
        results = data.get("results", [])
        total_count = data.get("totalHits", 0)
        
        books = []
        for item in results:
            # 1. Autoren parsen
            # CORE liefert: [{'name': 'Author 1'}, {'name': 'Author 2'}]
            author_list_raw = item.get("authors", [])
            authors = [a.get("name") for a in author_list_raw if a.get("name")]
            
            # 2. Titel
            title = item.get("title", "Unknown Title")
            
            # 3. Jahr
            year = str(item.get("yearPublished")) if item.get("yearPublished") else "-"
            
            # 4. Publisher / Journal / Repository
            # Wir nehmen den Publisher oder den Namen des Journals
            publisher = item.get("publisher") or "-"
            
            # 5. Link zum PDF/Download (Missbrauchen wir das ISBN Feld oder fügen wir ein neues Feld Link hinzu?)
            # Fürs erste packen wir den Link hinter den Publisher, ähnlich wie die ISBN
            download_url = item.get("downloadUrl", "")
            if download_url:
                # Wir formatieren es so, dass der Formatter es vielleicht erkennt oder einfach anzeigt
                publisher += f" | Link: {download_url}"

            books.append(
                Book(
                    title=title,
                    author=authors,
                    year=year,
                    publisher=publisher,
                    isbn=None # Papers haben selten eine ISBN, eher DOI (könnten wir später einbauen)
                )
            )

        return SearchResult(tracks=books, total=total_count, source="core")

    except Exception as e:
        print(f"DEBUG CORE: Fehler bei Request: {e}")
        return SearchResult(tracks=[], total=0, source="core")
