from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QFormLayout, QComboBox, QPushButton
from utils.key_points import key_points

class PointComboBox(QWidget):
    def __init__(self, parent, point_name: str):
        """Widget with combobox containing all Openpose keypoint labels

        Args:
            point_name (str): Name of point description to display to user (e.g. "point1")
        """
        super().__init__(parent)

        layout = QFormLayout()
        self.setLayout(layout)

        self.point_label = QLabel(point_name)
        self.points = QComboBox(self)
        self.points.addItems(key_points.keys())

        layout.addWidget(self.point_label)
        layout.addWidget(self.points)

    def name(self) -> str:
        """Returns the name of the currently selected point

        Returns:
            str: _description_
        """
        return self.points.currentText()