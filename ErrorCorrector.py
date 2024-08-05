import glob

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QPixmap, QDoubleValidator, QIntValidator, QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, \
    QFormLayout, QCheckBox
from geojson import Point, Feature, FeatureCollection, dump

from random import randint
from configs import config as config
import geojson
import os
import cv2
class ErrorCorrector(QWidget):
    def __init__(self):
        super().__init__()
        #layout = QVBoxLayout()
        self.setGeometry(0, 0, 1200, 600)



        # creating label
        self.label = QLabel(self)
        # loading image

        # adding image to label

        self.label.resize(960, 540)
        self.files_geojson = sorted(glob.glob(rf'./errorData/*.geojson'))
        self.files_img = sorted(glob.glob(rf'./errorData/*.jpg'))
        self.current_index = 0
        self.pixmap = QPixmap(self.files_img[self.current_index])
        self.label.setPixmap(self.pixmap)
        with open(self.files_geojson[self.current_index]) as f:
            data = geojson.load(f)
        feature =  data['features'][0]

        self.label_dir = QLabel('Тип', self)
        self.label_dir.setGeometry(1000, 35, 1000, 20)

        self.textbox_type = QLineEdit(self)
        self.textbox_type.move(1040, 35)
        self.textbox_type.resize(40, 20)
        self.textbox_type.setText("Тип")

        self.checkbox_side = QCheckBox("Боковой", self)
        self.checkbox_side.move(1000, 55)
        self.setWindowTitle("QLineEdit Example")

        self.label_dir = QLabel('Текст', self)
        self.label_dir.setGeometry(1000, 75, 1000, 20)

        self.textbox_text = QLineEdit(self)
        self.textbox_text.move(1040, 75)
        self.textbox_text.resize(40, 20)
        self.textbox_text.setText("Текст")


        self.button_prev = QPushButton("Назад", self)
        self.button_prev.move(430, 540)
        self.button_prev.clicked.connect(self.prev)

        self.button_next = QPushButton("Вперед", self)
        self.button_next.move(560, 540)
        self.button_next.clicked.connect(self.next)
        print(feature)
    def create_player(self):
        video = QVideoWidget(self)
        video.setVisible(True)
        video.resize(960, 540)
        video.move(0, 0)

    def next(self):
        if self.current_index == len(self.files_geojson) - 1:
            self.current_index = 0
        else:
            self.current_index += 1
        print(self.current_index )
        self.set_data()
    def prev(self):
        if self.current_index == 0:
            self.current_index = len(self.files_geojson) - 1
        else:
            self.current_index -= 1
        print(self.current_index)
        self.set_data()

    def set_data(self):
        with open(self.files_geojson[self.current_index]) as f:
            data = geojson.load(f)
        feature =  data['features'][0]
        self.pixmap = QPixmap(self.files_img[self.current_index])
        self.label.setPixmap(self.pixmap)
def get_error_sign():
    result = []
    with open(config.PATH_TO_GEOJSON) as f:
        data =  geojson.load(f)
    counter = 0

    for feature in data['features']:
        for item in feature["properties"]:
            features = []
            number_frame = None
            if item == 'MVALUE' and feature["properties"]['MVALUE'] == "":
                number_frame = float(feature["properties"]['num']) - 70
                result.append(feature)
            if feature["properties"]['type'] == "5.8.1":
                number_frame = float(feature["properties"]['num']) - 70
                result.append(feature)
            if feature["properties"]['type'] == "3.1" or feature["properties"]['type'] == "3.2":
                number_frame = float(feature["properties"]['num']) - 70
                result.append(feature)
            if number_frame != None:
                print(feature["properties"])

                features.append(Feature(geometry=feature["geometry"], properties=feature["properties"]))
                feature_collection = FeatureCollection(features)

                number_video = int(number_frame // 63600)
                number_frame_for_save = int(number_frame % 63600) + 50
                files = os.listdir(config.PATH_TO_VIDEO)
                new_path = os.path.join(config.PATH_TO_VIDEO, str(files[number_video]))
                cap = cv2.VideoCapture(new_path)
                cap.set(cv2.CAP_PROP_POS_FRAMES, number_frame_for_save)
                ret, frame = cap.read()
                while not ret:
                    ret, frame = cap.read()
                frame = cv2.resize(frame, dsize=(960, 540))
                cv2.imshow("frame",frame)
                cv2.imwrite(rf'./errorData/{str(counter)}.jpg', frame)
                with open(rf'./errorData/{str(counter)}.geojson', 'w') as f:
                    dump(feature_collection, f)
                cv2.waitKey(1000)
                counter += 1
                break
#get_error_sign()

import uuid
