# ui/side_bar.py
from PySide6.QtWidgets import(
    QDockWidget, 
    QListWidget, 
    QWidget,
    QGridLayout,
    QComboBox,
    QLabel,
    QSpinBox,
    QFrame
)

from PySide6.QtCore import Qt, Signal

class SideBar(QDockWidget):

    searchRequestet = Signal(str, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        content = QWidget(self)
        self.setWidget(content)

        layout = QGridLayout(content)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setVerticalSpacing(10)

        # Search input
        self.search_input = QComboBox()
        self.search_input.setEditable(True)
        self.search_input.setInsertPolicy(QComboBox.InsertAtTop)
        self.search_input.setMaxCount(50)
        self.search_input.setPlaceholderText("Search for music-term")
        self.search_input.setDuplicatesEnabled(False)
        self.search_input.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.search_input.lineEdit().returnPressed.connect(self.emit_search)

        # ----- Limit input -----
        self.limit_label = QLabel("Result limit:")
        self.limit_input = QSpinBox()
        self.limit_input.setRange(1, 100)
        self.limit_input.setValue(5)
        self.limit_input.setSingleStep(1)


        # ----- History -----
        self.history_label = QLabel("Search History")
        self.history_list = QListWidget()
        self.history_list.setMinimumHeight(120)

        # ----- Layout placement -----
        layout.addWidget(self.search_input, 0, 0)
        layout.addWidget(self.limit_label, 1, 0)
        layout.addWidget(self.limit_input, 2, 0)
        
        layout.addWidget(QFrame(frameShape=QFrame.HLine), 3, 0)

        layout.addWidget(self.history_label, 4, 0)
        layout.addWidget(self.history_list, 5, 0)

        # Stretch: only history grows
        layout.setRowStretch(5, 1)

    # add search term to history 
    def add_to_history(self, query: str):
        if not query:
            return
        # fileter duplicates
        for i in range(self.history_list.count()):
            if self.history_list.item(i).text() == query:
                return
        self.history_list.insertItem(0, query)


    # ----- Signals -----
    def emit_search(self):
       query = self.search_input.currentText().strip()
       limit = self.limit_input.value()
       self.searchRequestet.emit(query, limit)

    def clear_input(self):
        self.search_input.setCurrentText("")
            