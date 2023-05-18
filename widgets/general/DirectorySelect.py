from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit
from PyQt5.QtCore import Qt

class DirectorySelect(QWidget):
    """Widget for selecting directory of output folder

    Widgets:
        browse_btn: button to open file dialog
        filename_edit: line edit to contain the file path

    """
    def __init__(self, parent):
        super().__init__(parent)

        layout = QHBoxLayout()
        
        #Widgets
        browse_btn = QPushButton('Browse')
        browse_btn.clicked.connect(self.open_directory_dialog)

        self.filename_edit = QLineEdit()

        #Layout
        layout.addWidget(QLabel('Video and keypoint directory:'))
        layout.addWidget(self.filename_edit)
        layout.addWidget(browse_btn)

        self.setLayout(layout)


    def open_directory_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Directory of video and keypoints")

        if folder_path:
            self.filename_edit.setText(str(folder_path))