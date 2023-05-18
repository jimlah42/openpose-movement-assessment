from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit
from PyQt5.QtCore import Qt

from pathlib import Path

class VideoSelect(QWidget):
    def __init__(self, parent):
        """File select dialog for selecting unprocessed video

        Widgets:
            browse_btn: button to open file dialog
            filename_edit: line edit to contain the path of the video
        """
        super().__init__(parent)


        layout = QHBoxLayout()
        # directory selection
        browse_btn = QPushButton('Browse')
        browse_btn.clicked.connect(self.open_file_dialog)
        self.filename_edit = QLineEdit()

        layout.addWidget(QLabel('File:'))
        layout.addWidget(self.filename_edit)
        layout.addWidget(browse_btn)

        self.setLayout(layout)



    def open_file_dialog(self):
        filename, ok = QFileDialog.getOpenFileName(self, "Select input video", "./", "Videos (*.mp4 *.avi)")

        if filename:
            path = Path(filename)
            self.filename_edit.setText(str(path))