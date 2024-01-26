import json
import random
import time

from PyQt5.QtCore import QUrl
import cv2
from PyQt5.QtGui import QFont
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout,QMainWindow,QApplication,QLabel, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from qtpy import QtGui
#from architecture.View import View
from json import dump
from threading import Thread

import config
from Reader import Reader
from View import View
from CoordinateCalculation import CoordinateCalculation
from geojson import Point, Feature, FeatureCollection, dump, LineString
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #config.PATH_TO_VIDEO = r"D:\\Urban\\vid\\test\\GOPR0064"
        #config.PATH_TO_GPX = r"D:\\Urban\\vid\\test\\07,07,2021.gpx"
        #self.Reader = Reader(config.PATH_TO_GPX )
        self.calculation  = CoordinateCalculation()
        self.k = -0.3
        self.b = 10.83
        self.count_empty = 0
        self.counter_progress = 5000
        self.Reader = None
        self.is_play = True
        self.msgBox = None
        self.setGeometry(0, 0, 1200, 600)
        self.view = None
        self.thread = Thread(target=self.treatment, daemon=True)
        video = QVideoWidget(self)
        video.setVisible(True)
        video.resize(960, 540)
        video.move(0, 0)
        self.player = QMediaPlayer(self)
        self.player.setVolume(0)
        self.player.setVideoOutput(video)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("D:\\Urban\\vid\\2.mp4")))
        self.player.setPosition(0)
        self.player.play()

        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.setFont(QFont('Arial', 11))

        self.button_play = QPushButton("||", self)
        self.button_play.move(430, 540)
        self.button_play.clicked.connect(self.play)

        self.openDirButton = QPushButton("Open Directory", self)
        self.openDirButton.move(960,30)
        self.openDirButton.clicked.connect(self.getDirectory)

        self.button_open_GPX = QPushButton("open GPX", self)
        self.button_open_GPX.move(960, 60)
        self.button_open_GPX.clicked.connect(self.open_GPX)

        self.button_treatment = QPushButton("Начать обработку", self)
        self.button_treatment.move(960,  90)
        self.button_treatment.clicked.connect(self.thread.start)

        self.button_reproduce = QPushButton("Воспроизвести", self)
        self.button_reproduce.move(960, 120)

        self.button_open_save = QPushButton("open save", self)
        self.button_open_save.move(960, 150)
        self.button_open_save.clicked.connect(self.open_save)

        self.button_save_as = QPushButton("save as", self)
        self.button_save_as.move(960, 180)
        self.button_save_as.clicked.connect(self.save)

        self.button_save_as = QPushButton("Законьчить", self)
        self.button_save_as.move(960, 210)
        self.button_save_as.clicked.connect(self.final_data_processing)

        self.speed_frame_box = QLineEdit(self)
        self.speed_frame_box.move(960, 240)
        self.speed_frame_box.setText(str(config.FRAME_STEP))

        self.button_speed_frame = QPushButton("Выполнить", self)
        self.button_speed_frame.move(960, 270)
        self.button_speed_frame.clicked.connect(self.set_speed_frame)

        self.label_dir = QLabel('This is label', self)
        self.label_dir.setGeometry(1060, 35, 1000, 20)

        self.label_gpx = QLabel('This is label', self)
        self.label_gpx.setGeometry(1060, 65, 1000, 20)

        self.label_p = QLabel('0', self)
        self.label_p.setGeometry(1060, 95, 1000, 20)

        self.label = QLabel(self)
        self.pixmap = QPixmap('../cnt.png')
        self.label.resize(960, 540)

        self.show()
    def set_speed_frame(self):
        speed_value  = int(self.speed_frame_box.text())
        config.FRAME_STEP = speed_value
        self.speed_frame_box.setText(str(config.FRAME_STEP))
    def play(self):
        self.is_play = not self.is_play

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

    def showDialog(self):
        self.msgBox = QMessageBox()
        self.msgBox.setIcon(QMessageBox.Information)
        self.msgBox.setText("Файл сохранен")
        self.msgBox.setWindowTitle("Message")
        self.msgBox.setStandardButtons(QMessageBox.Ok)

    def save(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        save_path, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;json (*.json)", options=options)
        json = {
            'path_to_video' : config.PATH_TO_VIDEO,
            'frame_step': config.FRAME_STEP,
            'index_of_frame': config.INDEX_OF_FRAME,
            'count_processed_frames': config.COUNT_PROCESSED_FRAMES,
            'index_of_all_frame': config.INDEX_OF_All_FRAME,
            'index_of_gps': config.INDEX_OF_GPS,
            'index_of_video': config.INDEX_OF_VIDEO,
            'index_of_sing': config.INDEX_OF_SING,
            'path_to_geojson': config.PATH_TO_GEOJSON,
            'path_to_gpx':config.PATH_TO_GPX,
            'count_frame': config.COUNT_FRAMES,
            'classifier':  config.ClASSIFIER
        }
        with open(save_path, 'w') as f:
            dump(json, f)
        QMessageBox.about(self, "Сообщение", "Сохранено"  )


    def treatment(self):

        self.view = View()
        self.view.count_frames()
        count_gpx = self.Reader.get_count_dot()
        while self.view.cap.isOpened():
            speed = self.Reader.get_speed(config.INDEX_OF_GPS)
            print(config.FRAME_STEP, end='\r')
            try:
                ret, frame = self.view.cap.read()
                if ret == True:
                    config.FRAME_STEP = round(self.k * speed + self.b, 0)
                    #print(config.INDEX_OF_FRAME)
                    if self.count_empty > 5 :
                        config.FRAME_STEP += config.FRAME_STEP
                    self.view.cap.set(cv2.CAP_PROP_POS_FRAMES, config.INDEX_OF_FRAME)

                    config.INDEX_OF_FRAME += config.FRAME_STEP
                    config.INDEX_OF_All_FRAME += config.FRAME_STEP

                    self.label.setPixmap(self.convert_cv_qt(frame))
                    count_frame_for_gps =config.INDEX_OF_All_FRAME-  (config.INDEX_OF_GPS *60)
                    if self.counter_progress < config.INDEX_OF_All_FRAME:
                        #percent_frames = (config.INDEX_OF_All_FRAME * 100) / config.COUNT_FRAMES
                        #percent_gpx = (config.INDEX_OF_GPS * 100) / count_gpx
                        #print("percent_frames: ",round(percent_frames,2))
                        #print("percent_gpx: ",round(percent_gpx,2))
                        self.counter_progress += 5000

                    if count_frame_for_gps > 60 :
                        config.INDEX_OF_GPS += 1
                    if self.view.switch_video():
                        break

                    if round(speed,0) == 0:
                        continue
                    config.COUNT_PROCESSED_FRAMES += 1
                    retangles = self.view.draw_rectangles(frame)
                    self.label.setPixmap(self.convert_cv_qt(frame))
                    if not retangles:
                        self.count_empty += 1
                    else:
                        self.count_empty = 0

                    cv2.waitKey(1)
                cv2.waitKey(1)
                while not self.is_play:
                    pass
            except Exception as e:
                print("error", e)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(960, 540, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


    def open_GPX(self):
        gpx_path = QtWidgets.QFileDialog.getOpenFileName()
        config.PATH_TO_GPX = gpx_path[0].replace('/', '\\')
        self.Reader = Reader(config.PATH_TO_GPX )
        self.label_gpx.setText("<font color=black>" + str(config.PATH_TO_GPX) + "</font>")

    def getDirectory(self):
        dirlist = QFileDialog.getExistingDirectory(self,"Выбрать папку",".")
        config.PATH_TO_VIDEO = dirlist.replace('/', '\\') + "\\"
        self.label_dir.setText("{}".format(config.PATH_TO_VIDEO))
        self.Files = dirlist
    def final_data_processing(self):
        count = 0
        features = []
        path = r"D:\Urban\concat.geojson"

        grouped_objects = {}
        for obj in  self.view.sign_handler.result_sings:
            key = str(obj.car_coordinates_x[-1]) + str(obj.is_left)
            if key in grouped_objects:
                grouped_objects[key].append(obj)
            else:
                grouped_objects[key] = [obj]

        for key in grouped_objects:
            items = grouped_objects[key]
            coefficient = 2
            print('\n')
            for item in items:
                if len(item.car_coordinates_y) != 1:
                    x1, y1, x2, y2 = self.calculation.get_line(item, coefficient)
                    coefficient += 1
                    line = LineString([(y1, x1), (y2, x2)])
                    feature = Feature(geometry=line, properties={"type": f"{item.get_the_most_often(item.result_CNN)}"})
                    features.append(feature)
        feature_collection = FeatureCollection(features)

        with open(path, 'w', encoding='cp1251') as f:
            dump(feature_collection, f, skipkeys=False, ensure_ascii=True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
