from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from widgets.process.VideoSelect import VideoSelect
from widgets.process.PatientInfoForm import PatientInfoForm

from openpose.process_video import process_video

class ProcessWindow(QWidget):
    """This window is where you can process a raw video with openpose and input patient data

    Args:
        QWidget (_type_): _description_
    """
    def __init__(self, parent):
        super().__init__(parent)

        layout = QVBoxLayout()

        #Widgets
        self.file = VideoSelect(self)

        self.patient_info_form = PatientInfoForm(self)
        
        self.process_btn = QPushButton("Process Video")
        self.process_btn.clicked.connect(self.process)

        #Layout
        layout.addWidget(self.file)
        layout.addWidget(self.patient_info_form)
        layout.addWidget(self.process_btn)

        self.setLayout(layout)

    def process(self):
        print(self.file.filename_edit.text())
        patient_info = {
            "height": self.patient_info_form.p_height.text()
        }
        process_video(self.file.filename_edit.text(), patient_info)

