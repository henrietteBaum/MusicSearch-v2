# app/ui/search_frame.py

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox
)
from PySide6.QtCore import Signal


class SearchFrame(QWidget):
    search_requested = Signal(str, str) # search term, limit
    clear_requested = Signal()

    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        self.setLayout(layout)

        # Search History
        self.search_input = QComboBox(self)
        self.search_input.setEditable(True)
        self.search_input.setInsertPolicy(QComboBox.InsertAtTop)
        self.search_input.setMaxCount(50)

        # Search Limit
        self.limit_input = QLineEdit(self)
        self.limit_input.setPlaceholderText("10")
        self.limit_input.setFixedWidth(50)

        # Button
        self.search_button = QPushButton("Search", self)
        self.clear_button = QPushButton("Clear", self)

        # Grid Layout
        layout.addWidget(QLabel("Search Term:"), 0, 0)
        layout.addWidget(self.search_input, 0, 1)
        layout.addWidget(QLabel("Max Results:"), 0, 2)
        layout.addWidget(self.limit_input, 0, 3)
        layout.addWidget(self.search_button, 0, 4)
        layout.addWidget(self.clear_button, 0, 5)

        # Connect signals
        self.search_button.clicked.connect(self.on_search_clicked)
        self.clear_button.clicked.connect(self.clear_requested.emit)
        self.search_input.lineEdit().returnPressed.connect(self.on_search_clicked)

    def on_search_clicked(self):
        term = self.search_input.currentText().strip()
        limit_text = self.limit_input.text().strip()
        if not term:
            return
        try:
            limit = int(limit_text)
            if limit < 1:
                limit = 6
                limit_text = "6"
        except ValueError:
                limit_text = 4

        self.search_requested.emit(term, limit_text)
        
        # Felder leeren
        #self.search_input.clear()
        self.limit_input.clear()                                                                                               

    def clear_inputs(self):
         self.search_input.clear()
         self.limit_input.clear()
         self.search_input.setFocus()