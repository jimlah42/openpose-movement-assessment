from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QFormLayout, QComboBox, QPushButton
from widgets.measure.DistanceParamerters import DistanceParameters
from widgets.measure.AngleParameters import AngleParameters

class AddMeasurementForm(QWidget):
    def __init__(self, parent: QWidget):
        """Form widget to create new measurement, toggles input parameters based of type selected

        Widgets:
            name_input: Line edit containing name
            choose_type: Combo box containing type
            add_btn: button to be connected to measurement adding
            delete_btn: button to be connected to measurement deleting
            {measurement}_parameters: parameters widget for given measurement type
        """
        super().__init__(parent)

        self.layout = QFormLayout()

        #Widgets
        #Name
        name_label = QLabel("Name:")
        self.name_input = QLineEdit(self)

        #Type
        type_label = QLabel("Type:")
        self.choose_type = QComboBox(self)
        self.choose_type.addItems(["Distance", "Angle"])

        self.choose_type.currentTextChanged.connect(self.type_changed)
        
        self.add_btn = QPushButton("Add")
        self.delete_btn = QPushButton("Delete")

        self.distance_parameters = DistanceParameters(self)
        self.angle_parameters = AngleParameters(self)
        self.angle_parameters.hide()

        #Layout
        self.layout.addWidget(name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(type_label)
        self.layout.addWidget(self.choose_type)
        self.layout.addWidget(self.distance_parameters)
        self.layout.addWidget(self.angle_parameters)
        self.layout.addWidget(self.add_btn)
        self.layout.addWidget(self.delete_btn)

        self.setLayout(self.layout)

    def type_changed(self):
        if self.choose_type.currentText() == "Distance":
            self.distance_parameters.show()
            self.angle_parameters.hide()
            
        elif self.choose_type.currentText() == "Angle":
            self.angle_parameters.show()
            self.distance_parameters.hide()
