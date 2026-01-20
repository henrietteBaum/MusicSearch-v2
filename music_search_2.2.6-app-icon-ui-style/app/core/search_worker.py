# core/search_worker.py

from PySide6.QtCore import QThread, Signal
from core.search import search_all
from core.models import SearchDomain, SearchResult

class SearchWorker(QThread):
    # Signal liefert das fertige Dictionary, mit Ergebnissen, das wir zurücksenden
    results_ready = Signal(dict)

    def __init__(self, query: str, limit: int, domain: SearchDomain, mode:str):
        super().__init__()
        self.query = query
        self.limit = limit
        self.domain = domain
        self.mode = mode # <--- NEU: Wir speichern den Modus

    def run(self):
        """Hier wird die blockierende Suche ausgeführt."""
        try:
            # Hier rufen wir die zentrale Suchfunktion auf und geben den Modus weiter
            results = search_all(self.query, self.limit, self.domain, self.mode)
            self.results_ready.emit(results)
        except Exception as e:
            print(f"DEBUG Worker: Schwerer Fehler in der Hintergrundsuche: {e}")
            # Optional: Ein leeres Dictionary senden, damit die App nicht hängt
            self.results_ready.emit({})