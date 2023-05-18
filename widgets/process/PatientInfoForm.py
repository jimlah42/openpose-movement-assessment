from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QFormLayout

class PatientInfoForm(QWidget):
    def __init__(self, parent: QWidget):
        """Form widget for collecting patient data needed for processing

        Widgets:
        p_height: line edit containing patient height
        """
        super().__init__(parent)


        self.p_height = QLineEdit()

        layout = QFormLayout()

        layout.addRow(QLabel("Height (cm):"), self.p_height)

        self.setLayout(layout)