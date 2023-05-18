from PyQt5.QtWidgets import QWidget, QGridLayout, QListWidget, QPushButton
from widgets.measure.AddMeasurementForm import AddMeasurementForm
from widgets.general.DirectorySelect import DirectorySelect
from measurements.DistanceMeasurement import DistanceMeasurement
from measurements.AngleMeasurement import AngleMeasurement
from measurements.calculate_measurements import calculate
from measurements.measurement_tools import get_measurement_objects
from draw.draw_tools import draw_measurements
from widgets.general.ProcessDialogs import SucessDialog

class MeasurementsWindow(QWidget):
    """This window is where you can add and delete measurements to a file then process them to json and draw them onto video
    """
    def __init__(self, parent):
        super().__init__(parent)

        layout = QGridLayout()

        #Widgets
        self.measurement_list = QListWidget(self)
        self.measurements = []

        self.add_measurement_form = AddMeasurementForm(self)
        self.add_measurement_form.setEnabled(False)
        self.add_measurement_form.add_btn.clicked.connect(self.add_measurement)
        self.add_measurement_form.delete_btn.clicked.connect(self.delete_measurement)

        self.process_btn = QPushButton("Process")
        self.process_btn.setEnabled(False)
        self.process_btn.clicked.connect(self.process_measurements)

        self.draw_btn = QPushButton("Draw")
        self.draw_btn.setEnabled(False)
        self.draw_btn.clicked.connect(self.process_drawing)

        self.directory_select = DirectorySelect(self)
        self.directory_select.filename_edit.textChanged.connect(self.load_measurements)

        #Layout
        layout.addWidget(self.measurement_list, 0, 0)
        layout.addWidget(self.add_measurement_form, 0, 1)
        layout.addWidget(self.directory_select, 1, 0)
        layout.addWidget(self.process_btn, 1, 1, 1, 1)
        layout.addWidget(self.draw_btn, 1, 2, 1, 1)

        self.setLayout(layout)



    def load_measurements(self):
        if (self.directory_select.filename_edit.text() != ""):
            self.process_btn.setEnabled(True)
            self.draw_btn.setEnabled(True)
            self.add_measurement_form.setEnabled(True)

        self.measurement_list.clear()
        self.measurements = get_measurement_objects(self.directory_select.filename_edit.text())
        print(self.measurements)

        for measurement in self.measurements:
            self.measurement_list.addItem(measurement.name + " : " + measurement.info_readable())

    def add_measurement(self):

        m_name: str = self.add_measurement_form.name_input.text()
        m_type: str = self.add_measurement_form.choose_type.currentText()

        if (m_type == "Distance"):
            params = self.add_measurement_form.distance_parameters
            measurement = DistanceMeasurement(m_name, params.point1.name(), params.point2.name())
        elif (m_type == "Angle"):
            params = self.add_measurement_form.angle_parameters
            measurement = AngleMeasurement(m_name, params.point1.name(), params.point2.name(), params.pivot.name())

        self.measurements.append(measurement)
        self.measurement_list.addItem(measurement.name + " : " + measurement.info_readable())
    
    def delete_measurement(self):
        listItems = self.measurement_list.selectedItems()
        if not listItems: return        
        for item in listItems:
            self.measurement_list.takeItem(self.measurement_list.row(item))
            self.measurements.pop(self.measurement_list.row(item))
    
    def process_measurements(self):
        res = calculate(self.directory_select.filename_edit.text(), self.measurements)
        SucessDialog(res).exec()



    def process_drawing(self):
        res = draw_measurements(self.directory_select.filename_edit.text(), self.measurements, True)
        SucessDialog(res).exec()
