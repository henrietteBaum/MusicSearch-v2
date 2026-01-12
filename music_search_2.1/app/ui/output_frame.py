# app/ui/output_frame.py

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QTextEdit,
    QVBoxLayout,
    QFrame,
)


class OutputFrame(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # iTunes 
        self.itunes_frame = QFrame(self)
        itunes_layout = QVBoxLayout(self.itunes_frame)
        self.itunes_label = QLabel("iTunes Results", self.itunes_frame)
        self.itunes_output = QTextEdit(self.itunes_frame)
        self.itunes_output.setReadOnly(True)
        self.itunes_output.setFrameStyle(QFrame.NoFrame)
        itunes_layout.addWidget(self.itunes_output)
        itunes_layout.addWidget(self.itunes_label)
        layout.addWidget(self.itunes_frame)

        # MusicBrainz
        self.mb_frame = QFrame(self)
        mb_layout = QVBoxLayout(self.mb_frame)
        self.mb_label = QLabel("MusicBrainz Results", self.mb_frame)
        self.mb_output = QTextEdit(self.mb_frame)
        self.mb_output.setReadOnly(True)
        self.mb_output.setFrameStyle(QFrame.NoFrame)
        mb_layout.addWidget(self.mb_output)
        mb_layout.addWidget(self.mb_label)
        layout.addWidget(self.mb_frame)

    def set_itunes_header(self, header: str):
        self.itunes_output.clear()
        self.itunes_output.append(header)

    def set_mb_header(self, header: str):
        self.mb_output.clear()
        self.mb_output.append(header)

    def show_itunes_results(self, tracks):
            #self.itunes_output.clear()
            for t in tracks:
                line = f"{t.artist} - {t.title}"
                if t.album:
                    line += f"Album: {t.album}\n"
                self.itunes_output.append(line)

    def show_mb_results(self, tracks):
            #self.mb_output.clear()
            for t in tracks:
                line = f"{t.artist} - {t.title}"
                if t.album:
                    line += f" ({t.album})"
                self.mb_output.append(line)

    def clear_outputs(self):
        self.itunes_output.clear()
        self.mb_output.clear()

        