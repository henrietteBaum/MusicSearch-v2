# core/search_worker.py

from PySide6.QtCore import QThread, Signal
from core.search import search_all
from core.models import SearchDomain, SearchResult

class SearchWorker(QThread):
    # Signal definiert das Dictionary, das wir zurücksenden
    results_ready = Signal(dict)

    def __init__(self, query: str, limit: int, domain: SearchDomain):
        super().__init__()
        self.query = query
        self.limit = limit
        self.domain = domain

    def run(self):
        """Hier wird die blockierende Suche ausgeführt."""
        try:
            results = search_all(self.query, self.limit, self.domain)
            self.results_ready.emit(results)
        except Exception as e:
            print(f"DEBUG Worker: Schwerer Fehler in der Hintergrundsuche: {e}")
            # Optional: Ein leeres Dictionary senden, damit die App nicht hängt
            self.results_ready.emit({})