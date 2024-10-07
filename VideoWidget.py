import os

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSlider,
    QStyle,
    QVBoxLayout,
    QWidget, QListWidget, QListWidgetItem,
)

from configs import config

class VideoPlayerWidget(QWidget):
    def __init__(self, server,  parent=None):
        super().__init__(parent)

        self.server = server
        self.index_of_video = 0
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Create layouts
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout_player = QVBoxLayout()
        layout_player.addWidget(self.videoWidget)
        layout_player.addLayout(controlLayout)
        layout_player.addWidget(self.errorLabel)

        self.listVideos = QListWidget()
        self.listVideos.setFixedWidth(100)
        for item in config.VIDEOS:
            QListWidgetItem(item, self.listVideos)
        self.listVideos.itemClicked.connect(self.change_video)

        layout = QHBoxLayout()
        layout.addLayout(layout_player)
        layout.addWidget(self.listVideos)
        self.setLayout(layout)
        # Connect signals
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)

        self.current_path_of_video = os.path.join(config.PATH_TO_VIDEO, config.VIDEOS[self.index_of_video])
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.current_path_of_video)))
        self.playButton.setEnabled(True)

        self.mediaPlayer.positionChanged.connect(self.change_dot)

    def change_dot(self):
        seconds_current_video = round(self.mediaPlayer.position()/1000,0)
        seconds_all_video =(self.index_of_video * 1060) + seconds_current_video
        config.SECONDES_ALL_VIDEO = seconds_all_video
        self.server.change_dot(int(seconds_all_video))
    def change_video(self, clicked_item):
        self.change_color_current_video(clicked_item)
        self.current_path_of_video = os.path.join(config.PATH_TO_VIDEO, clicked_item.text())
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.current_path_of_video)))
        self.index_of_video = config.VIDEOS.index(clicked_item.text())
        self.play()

    def change_color_current_video(self, clicked_item):
        for i in range(self.listVideos.count()):
            item = self.listVideos.item(i)
            item.setBackground(QtGui.QColor(255, 255, 255))
        clicked_item.setBackground(QtGui.QColor(234, 230, 202))

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
            )

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
