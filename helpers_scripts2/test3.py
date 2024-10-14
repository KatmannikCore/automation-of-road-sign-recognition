
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QComboBox, QLabel
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 800, 600)

        # Создаем виджет для видео
        self.video_widget = QVideoWidget()

        # Создаем медиаплеер
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)

        # Устанавливаем видео файл (замените на свой путь к видео)
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(r"E:\Urban\vid\test\GOPR0064\GOPR0064.mp4")))

        # Кнопки управления
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_video)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_video)

        # ComboBox для изменения скорости
        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["0.1x", "0.5x", "1.0x", "1.5x", "2.0x"])
        self.speed_combo.currentIndexChanged.connect(self.change_speed)

        self.speed_label = QLabel("Speed: 1.0x")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        layout.addWidget(self.play_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.speed_combo)
        layout.addWidget(self.speed_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def play_video(self):
        self.media_player.play()

    def stop_video(self):
        self.media_player.stop()

    def change_speed(self):
        speed_value = float(self.speed_combo.currentText().replace("x", ""))  # Извлекаем значение скорости
        self.media_player.setPlaybackRate(speed_value)
        self.speed_label.setText(f"Speed: {speed_value:.1f}x")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
