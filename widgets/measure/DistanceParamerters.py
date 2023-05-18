from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QFormLayout, QComboBox, QPushButton
from widgets.measure.PointComboBox import PointComboBox

class DistanceParameters(QWidget):
    """Form widget containing the inputs required to build a distance measurement object

    Widgets:
        point1: ComboBox to select keypoint label
        point2: ComboBox to select keypoint label
    """

    def __init__(self, parent):
        super().__init__(parent)
        layout = QFormLayout()

        self.point1 = PointComboBox(self, "Point 1")
        self.point2 = PointComboBox(self, "Point 2")

        layout.addWidget(self.point1)
        layout.addWidget(self.point2)
        self.setLayout(layout)