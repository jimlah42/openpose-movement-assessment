from PyQt5.QtWidgets import QWidget, QGridLayout, QListWidget, QPushButton, QListWidgetItem, QLineEdit, QLabel
from PyQt5.QtCore import Qt
from widgets.general.DirectorySelect import DirectorySelect
from data.data_tools import get_measurement_names, generate_csv, generate_plot

class AnalyseWindow(QWidget):
    """This window is where you can generate graphs and csv data of a given video

    Args:
        QWidget (_type_): _description_
    """
    def __init__(self, parent):
        super().__init__(parent)

        layout = QGridLayout()

        #Widgets
        self.input_dir = DirectorySelect(self)
        self.all_measurements = []
        self.selected_measurements = []

        self.input_dir.filename_edit.textChanged.connect(self.load_dir)

        self.measurement_list = QListWidget(self)
        self.measurement_list.itemClicked.connect(self.check_item)

        self.generate_label = QLabel("Output Filename")
        self.csv_filename = QLineEdit("data", self)
        self.generate_btn = QPushButton("Generate CSV")
        self.generate_btn.clicked.connect(self.generate)

        self.plot_label = QLabel("Plot Title")
        self.plot_title = QLineEdit("Title", self)
        self.plot_btn = QPushButton("Plot")
        self.plot_btn.clicked.connect(self.plot)

        #Layout
        layout.addWidget(self.input_dir)
        layout.addWidget(self.measurement_list)
        layout.addWidget(self.generate_label)
        layout.addWidget(self.csv_filename)
        layout.addWidget(self.generate_btn)
        layout.addWidget(self.plot_label)
        layout.addWidget(self.plot_title)
        layout.addWidget(self.plot_btn)

        self.setLayout(layout)
    

    def load_dir(self):
        self.measurement_list.clear()
        
        self.all_measurements = get_measurement_names(self.input_dir.filename_edit.text())

        for measurement in self.all_measurements:
            item = QListWidgetItem(str(measurement))
            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable)
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.measurement_list.addItem(item)
        print(self.all_measurements)

    def check_item(self):
        curr_item = self.measurement_list.currentItem() 
        if (curr_item.checkState() == Qt.CheckState.Checked):
            curr_item.setCheckState(Qt.CheckState.Unchecked)
        else:
            curr_item.setCheckState(Qt.CheckState.Checked)

    def generate(self):
        for i in range(self.measurement_list.count()):
            item = self.measurement_list.item(i)
            if (item.checkState() == Qt.CheckState.Checked):
                self.selected_measurements.append(item.text())

        generate_csv(self.input_dir.filename_edit.text(), self.selected_measurements, self.csv_filename.text())

    def plot(self):
        self.selected_measurements.clear()
        for i in range(self.measurement_list.count()):
            item = self.measurement_list.item(i)
            if (item.checkState() == Qt.CheckState.Checked):
                self.selected_measurements.append(item.text())
        
        generate_plot(self.input_dir.filename_edit.text(), self.plot_title.text(), self.selected_measurements)

