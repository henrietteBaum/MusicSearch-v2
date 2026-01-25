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
        self.search_label = QLabel("Search for term:")
        self.search_input = QComboBox()
        self.search_input.setEditable(True)
        self.search_input.setInsertPolicy(QComboBox.InsertAtTop)
        self.search_input.setMaxCount(50)
        self.search_input.setPlaceholderText("Search for music-term")
        #self.search_input.setAccessibleDescription("Enter search-term.")
        self.search_input.setDuplicatesEnabled(False)
        self.search_input.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.search_input.lineEdit().returnPressed.connect(self.emit_search)
        self.search_label.setBuddy(self.search_input)

        # ----- Limit input -----
        self.limit_label = QLabel("Result limit:")
        self.limit_input = QSpinBox()
        self.limit_input.setSuffix(" max. results")
        #self.limit_input.setAccessibleDescription("Enter search-limit")
        self.limit_input.setRange(1, 100)
        self.limit_input.setValue(5)
        self.limit_input.setSingleStep(1)
        self.limit_input.editingFinished.connect(self.emit_search)
        self.limit_label.setBuddy(self.limit_input)

        # ----- History -----
        self.history_label = QLabel("Search History")
        self.history_list = QListWidget()
        self.history_list.setMinimumHeight(120)
        self.history_list.setAccessibleName("Search history list.")
        self.history_list.itemActivated.connect(self.on_history_item_activated)
        self.history_list.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.history_label.setBuddy(self.history_list)

        # ----- Layout placement -----
        layout.addWidget(self.search_label, 0, 0)
        layout.addWidget(self.search_input, 1, 0)
        layout.addWidget(self.limit_label, 2, 0)
        layout.addWidget(self.limit_input, 3, 0)
        
        layout.addWidget(QFrame(frameShape=QFrame.HLine), 4, 0)

        layout.addWidget(self.history_label, 5, 0)
        layout.addWidget(self.history_list, 6, 0)

        # Stretch: only history grows
        layout.setRowStretch(6, 1)

    # add search term to history 
    def add_to_history(self, query: str):
        if not query:
            return
        # fileter duplicates
        for i in range(self.history_list.count()):
            if self.history_list.item(i).text() == query:
                self.history_list.takeItem(i)
                break
                #return
        self.history_list.insertItem(0, query)

        new_item = self.history_list.item(0)
        self.history_list.setCurrentItem(new_item)

    def on_history_item_activated(self, item):
        search_term = item.text()
        self.search_input.setCurrentText(search_term)
        self.emit_search()


    # ----- Signals -----
    def emit_search(self):
       query = self.search_input.currentText().strip()
       limit = self.limit_input.value()
       self.searchRequestet.emit(query, limit)

    def clear_input(self):
        self.search_input.setCurrentText("")
            