from PyQt5.QtWidgets import QWidget, QVBoxLayout

from widgets.view.VideoPlayer import VideoPlayer


class ViewWindow(QWidget):
    """This window is where you can load and view a video
    """
    def __init__(self, parent):
        super().__init__(parent)

        layout = QVBoxLayout()

        #Widgets
        video_player = VideoPlayer(self)

        #Layout
        layout.addWidget(video_player)

        self.setLayout(layout)