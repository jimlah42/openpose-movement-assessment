from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QWidget, QPushButton, QStyle, QVBoxLayout, QFileDialog, QSlider
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer

class VideoPlayer(QWidget):
    """Media Player widget for viewing videos with playback controls
    """
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        video = QVideoWidget()

        self.position_slider = QSlider(Qt.Horizontal)        
        self.position_slider.setRange(0,0)
        self.position_slider.sliderMoved.connect(self.set_position)

        self.play_btn = QPushButton()
        self.play_btn.setEnabled(False)
        self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_btn.clicked.connect(self.play)

        self.open_video_btn = QPushButton("Open Video")
        self.open_video_btn.clicked.connect(self.open_file)

        self.media_player.setVideoOutput(video)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.positionChanged.connect(self.position_changed)

        layout = QVBoxLayout()

        layout.addWidget(video)
        layout.addWidget(self.position_slider)
        layout.addWidget(self.play_btn)
        layout.addWidget(self.open_video_btn)

        self.setLayout(layout)

    def play(self):
        if self.media_player.state() == QMediaPlayer.State.PlayingState:
            self.media_player.pause()
            self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.media_player.play()
            self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
    
    def open_file(self):

        file_name, ok = QFileDialog.getOpenFileName(self, "Select input video (only works with .avi files)", "./", "Videos (*.avi)")

        if (file_name != ''):
            print(file_name)
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_name)))
            self.play_btn.setEnabled(True)

    def set_position(self, position):
        self.media_player.setPosition(position)

    def duration_changed(self, duration):
        self.position_slider.setRange(0, duration)

    def position_changed(self, position):
        self.position_slider.setValue(position)