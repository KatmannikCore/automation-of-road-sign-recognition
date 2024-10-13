import json
import os
from json import dump
from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QLabel, QMessageBox
from PyQt5.QtWidgets import QPushButton
from geojson import dump
from Converter import Converter
from GPXHandler import GPXHandler
from configs import config


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.converter = Converter()

        self.calculation = None
        self.k = -0.5
        self.b = 10.9
        self.count_empty = 0
        self.counter_progress = 5000
        self.GPXHandler = None
        self.is_wait = False
        self.is_brake = False
        self.msgBox = None
        self.setGeometry(0, 0, 1200, 600)
        self.view = None

        #self.create_player()
        self.create_text()
        self.create_buttons()
        self.set_path_to_video()
        self.show()

    def create_player(self):
        video = QVideoWidget(self)
        video.setVisible(True)
        video.resize(960, 540)
        video.move(0, 0)

        self.player = QMediaPlayer(self)
        self.player.setVolume(0)
        self.player.setVideoOutput(video)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(rf"D:\video\GP10064.mp4")))
        self.player.setPosition(0)
        self.player.play()

        self.label = QLabel(self)
        self.label.resize(960, 540)

    def create_text(self):
        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.setFont(QFont('Arial', 11))

        self.label_dir = QLabel('', self)
        self.label_dir.setGeometry(1060, 35, 1000, 20)

        self.label_gpx = QLabel('', self)
        self.label_gpx.setGeometry(1060, 65, 1000, 20)

        self.label_geojson = QLabel('', self)
        self.label_geojson.setGeometry(1060, 90, 1000, 20)

    def create_buttons(self):
        self.button_play = QPushButton("||", self)
        self.button_play.move(430, 540)
        self.button_play.clicked.connect(self.play)

        self.button_choose_dir = QPushButton("Открыть папку", self)
        self.button_choose_dir.move(960, 30)

        self.button_choose_GPX = QPushButton("Открыть GPX", self)
        self.button_choose_GPX.move(960, 60)

        self.button_choose_geojson = QPushButton("Выбрать geojson", self)
        self.button_choose_geojson.move(960, 90)

        self.button_treatment = QPushButton("Начать обработку", self)
        self.button_treatment.move(960, 120)

        #self.button_open_save = QPushButton("open save", self)
        #self.button_open_save.move(960, 150)
        #self.button_open_save.clicked.connect(self.open_save)

        #self.button_save_as = QPushButton("save as", self)
        #self.button_save_as.move(960, 180)
        #self.button_save_as.clicked.connect(self.save)

        self.button_end = QPushButton("Закончить", self)
        self.button_end.move(960, 210)
        self.button_end.setEnabled(False)

        #self.speed_frame_box = QLineEdit(self)
        #self.speed_frame_box.move(960, 240)
        #self.speed_frame_box.setText(str(config.FRAME_STEP))

        #self.button_speed_frame = QPushButton("Выполнить", self)
        #self.button_speed_frame.move(960, 270)
        #self.button_speed_frame.clicked.connect(self.set_speed_frame)

        self.button_corrector = QPushButton("Ошибки", self)
        self.button_corrector.move(630, 540)

        self.button_viewTrack = QPushButton("Карта", self)
        self.button_viewTrack.move(730, 540)

    def set_path_to_video(self):
        config.PATH_TO_GPX = r"D:\13,03,24-Деревная.gpx"
        self.GPXHandler = GPXHandler()
        self.label_gpx.setText("<font color=black>" + str(config.PATH_TO_GPX) + "</font>")

        config.PATH_TO_VIDEO = r"D:\video" + "\\"
        config.VIDEOS = os.listdir(config.PATH_TO_VIDEO)
        self.label_dir.setText("{}".format(config.PATH_TO_VIDEO))
        self.Files = os.listdir(config.PATH_TO_VIDEO)
        config.PATH_TO_GEOJSON = r"D:\Деревная.geojson"
        self.label_geojson.setText("{}".format(config.PATH_TO_GEOJSON))


    #TODO Не используется
    def set_speed_frame(self):
        speed_value = int(self.speed_frame_box.text())
        config.FRAME_STEP = speed_value
        self.speed_frame_box.setText(str(config.FRAME_STEP))

    def play(self):
        self.is_wait = not self.is_wait

    # TODO Не используется
    def open_save(self):
        open_save_path = QtWidgets.QFileDialog.getOpenFileName()
        with open(open_save_path[0]) as f:
            templates = json.load(f)
            config.PATH_TO_VIDEO = templates['path_to_video']
            config.FRAME_STEP = templates['frame_step']
            config.INDEX_OF_FRAME = templates['index_of_frame']
            config.COUNT_PROCESSED_FRAMES = templates['count_processed_frames']
            config.INDEX_OF_All_FRAME = templates['index_of_all_frame']
            config.INDEX_OF_GPS = templates['index_of_gps']
            config.INDEX_OF_VIDEO = templates['index_of_video']
            config.INDEX_OF_SING = templates['index_of_sing']
            config.PATH_TO_GEOJSON = templates['path_to_geojson']
            config.PATH_TO_GPX = templates['path_to_gpx']
            config.COUNT_FRAMES = templates['count_frame']
            config.ClASSIFIER = templates['classifier']
        self.label_dir.setText("<font color=black>" + str(config.PATH_TO_VIDEO) + "</font>")
        self.label_gpx.setText("<font color=black>" + str(config.PATH_TO_GPX) + "</font>")

        self.thread.start()

    # TODO Не используется
    def showDialog(self):
        self.msgBox = QMessageBox()
        self.msgBox.setIcon(QMessageBox.Information)
        self.msgBox.setText("Файл сохранен")
        self.msgBox.setWindowTitle("Message")
        self.msgBox.setStandardButtons(QMessageBox.Ok)

    # TODO Не используется
    def save(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        save_path, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                   "All Files (*);;json (*.json)", options=options)
        json = {
            'path_to_video': config.PATH_TO_VIDEO,
            'frame_step': config.FRAME_STEP,
            'index_of_frame': config.INDEX_OF_FRAME,
            'count_processed_frames': config.COUNT_PROCESSED_FRAMES,
            'index_of_all_frame': config.INDEX_OF_All_FRAME,
            'index_of_gps': config.INDEX_OF_GPS,
            'index_of_video': config.INDEX_OF_VIDEO,
            'index_of_sing': config.INDEX_OF_SING,
            'path_to_geojson': config.PATH_TO_GEOJSON,
            'path_to_gpx': config.PATH_TO_GPX,
            'count_frame': config.COUNT_FRAMES,
            'classifier': config.ClASSIFIER
        }
        with open(save_path, 'w') as f:
            dump(json, f, ensure_ascii=False)
        QMessageBox.about(self, "Сообщение", "Сохранено")
