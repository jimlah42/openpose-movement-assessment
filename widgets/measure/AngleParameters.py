from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QFormLayout, QComboBox, QPushButton
from widgets.measure.PointComboBox import PointComboBox

class AngleParameters(QWidget):
    def __init__(self, parent):
        """Form widget containing the inputs required to build an angle measurement object

        Widgets:
            point1: ComboBox to select keypoint label
            point2: ComboBox to select keypoint label
            pivot: ComboBox to select keypoint label

        """
        super().__init__(parent)
        self.layout = QFormLayout()

        self.point1 = PointComboBox(self, "Point 1")
        self.point2 = PointComboBox(self, "Point 2")
        self.pivot = PointComboBox(self, "Pivot")

        self.layout.addWidget(self.point1)
        self.layout.addWidget(self.point2)
        self.layout.addWidget(self.pivot)
        self.setLayout(self.layout)