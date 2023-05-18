from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QLabel

class SucessDialog(QDialog):
    def __init__(self, sucess: bool) -> None:
        """Dialog to indicate the sucess or failure of a process

        Args:
            sucess (bool): True for sucess message False for failure message
        """
        super().__init__()
    
        self.setWindowTitle("Process")

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.accept)

        layout = QVBoxLayout()

        if (sucess):
            message = QLabel("Processed Sucessfully")
        else: 
            message = QLabel("Something went wrong")

        layout.addWidget(message)
        layout.addWidget(self.button_box)

        self.setLayout(layout)
