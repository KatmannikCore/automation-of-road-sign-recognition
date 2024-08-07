import glob

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QPixmap, QDoubleValidator, QIntValidator, QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, \
    QFormLayout, QCheckBox
from geojson import Point, Feature, FeatureCollection, dump

from random import randint

from ChangerType import ChangerType
from configs import config as config
import geojson
import os
import cv2


class ErrorCorrector(QWidget):
    def __init__(self):
        super().__init__()
        #layout = QVBoxLayout()
        self.setGeometry(0, 0, 1200, 600)
        self.ChangerType = ChangerType()

        self.ChangerType.list_widget.itemClicked.connect(self.change_type)

        # creating label
        self.label = QLabel(self)

        self.label.resize(960, 540)
        self.files_geojson = sorted(glob.glob(rf'./errorData/*.geojson'))
        self.files_img = sorted(glob.glob(rf'./errorData/*.jpg'))
        self.current_index = 0
        self.pixmap = QPixmap(self.files_img[self.current_index])
        self.label.setPixmap(self.pixmap)

        self.label_t = QLabel('Тип:', self)
        self.label_t.setGeometry(1000, 35, 1000, 20)

        self.label_img_type = QLabel(self)
        self.img_type = QPixmap(rf"D:\Urban\map\100\V1.1.png")
        self.label_img_type.setPixmap(self.img_type)
        self.label_img_type.resize(100, 100)
        self.label_img_type.move(1090, 0)

        self.label_type = QLabel('name', self)
        self.label_type.setGeometry(1025, 35, 1000, 20)

        self.checkbox_side = QCheckBox("Боковой", self)
        self.checkbox_side.move(1000, 85)

        self.label_dir = QLabel('Текст', self)
        self.label_dir.setGeometry(1000, 105, 1000, 20)

        self.textbox_text = QLineEdit(self)
        self.textbox_text.move(1040, 105)
        self.textbox_text.resize(80, 20)

        self.button_prev = QPushButton("Назад", self)
        self.button_prev.move(430, 540)
        self.button_prev.clicked.connect(self.prev)

        self.button_next = QPushButton("Вперед", self)
        self.button_next.move(560, 540)
        self.button_next.clicked.connect(self.next)

        self.button_next = QPushButton("Законьчить", self)
        self.button_next.move(1000, 540)
        self.button_next.clicked.connect(self.finish_correction)

        self.button_change_type = QPushButton("Изменить тип", self)
        self.button_change_type.move(1000, 55)
        self.button_change_type.clicked.connect(self.open_change_type_window)

        self.set_data()
        self.setWindowTitle("QLineEdit Example")

    #def finish_correction(self):

    def change_type(self, item):
        self.label_type.setText(item.text().replace("V", ""))
        self.img_type = QPixmap(rf"D:\Urban\map\100\{item.text()}.png")
        self.label_img_type.setPixmap(self.img_type)
        self.ChangerType.hide()
    def open_change_type_window(self):
        if self.ChangerType.isVisible():
            self.ChangerType.hide()
        else:
            self.ChangerType.show()


    def next(self):
        self.change_geojson()
        if self.current_index == len(self.files_geojson) - 1:
            self.current_index = 0
        else:
            self.current_index += 1
        self.set_data()

    def prev(self):
        self.change_geojson()
        if self.current_index == 0:
            self.current_index = len(self.files_geojson) - 1
        else:
            self.current_index -= 1
        self.set_data()

    def set_data(self):
        self.feature = self.get_feature_object()
        self.pixmap = QPixmap(self.files_img[self.current_index])
        self.label.setPixmap(self.pixmap)
        self.label_type.setText(self.feature["properties"]['type'])
        self.img_type = QPixmap(rf"D:\Urban\map\100\V{self.feature['properties']['type']}.png")
        self.label_img_type.setPixmap(self.img_type)

        if 'MVALUE' in self.feature["properties"]:
            self.textbox_text.setEnabled(True)
            self.textbox_text.setText(self.feature["properties"]["MVALUE"])
        else:
            self.textbox_text.setEnabled(False)
        self.checkbox_side.setChecked(self.feature["properties"]['side'] == "True")

    def get_feature_object(self):
        with open(self.files_geojson[self.current_index], encoding='utf-8') as f:
            data = geojson.load(f)
        return data['features'][0]

    def change_geojson(self):
        is_was_changes = False
        if self.feature["properties"]['type'] != self.label_type.text():
            self.feature["properties"]['type'] = self.label_type.text()
            is_was_changes = True
        if 'MVALUE' in self.feature["properties"]:
            if self.feature["properties"]['MVALUE'] != self.textbox_text.text():
                self.feature["properties"]['MVALUE'] = self.textbox_text.text()
                is_was_changes = True
        if self.feature["properties"]['side'] != str(self.checkbox_side.isChecked()):
            self.feature["properties"]['side'] = str(self.checkbox_side.isChecked())
            is_was_changes = True
        if is_was_changes:
            features = [Feature(geometry=self.feature["geometry"], properties=self.feature["properties"])]
            feature_collection = FeatureCollection(features)
            with open(self.files_geojson[self.current_index], 'w', encoding='utf-8') as f:
                dump(feature_collection, f)


def get_error_sign():
    result = []
    with open(config.PATH_TO_GEOJSON) as f:
        data = geojson.load(f)
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
                cv2.imshow("frame", frame)
                cv2.imwrite(rf'./errorData/{str(counter)}.jpg', frame)
                with open(rf'./errorData/{str(counter)}.geojson', 'w') as f:
                    dump(feature_collection, f)
                cv2.waitKey(1000)
                counter += 1
                break
