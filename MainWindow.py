from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QPushButton, QLineEdit, QLabel, QGridLayout, QFileDialog, QWidget, QTabWidget

import sys
from pathlib import Path

from ProcessWindow import ProcessWindow
from ViewWindow import ViewWindow
from MeasurementsWindow import MeasurementsWindow
from AnalyseWindow import AnalyseWindow


class MainWindow(QWidget):
    """Main winow of the app, contains the tabs of all other widows
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("OpenPose Movement Assessment")
        self.setFixedSize(QSize(800, 600))

        self.main_layout = QGridLayout(self)
        self.setLayout(self.main_layout)

        #Widgets
        process_window = ProcessWindow(self)
        measurements_window = MeasurementsWindow(self)
        analyse_window = AnalyseWindow(self)
        view_window = ViewWindow(self)

        self.tab = QTabWidget(self)
        self.tab.addTab(process_window, "Process Video")
        self.tab.addTab(measurements_window, "Measure / Visualise")
        self.tab.addTab(view_window, "View")
        self.tab.addTab(analyse_window, "Analyse")

        #Layout
        self.main_layout.addWidget(self.tab, 0,0,2,1)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())