import glob
import os
import time

import cv2
import geojson
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtWidgets import QPushButton, QLabel, QWidget, QLineEdit, \
    QCheckBox
from geojson import Feature, FeatureCollection, dump

from ChangerType import ChangerType
from CoordinateCalculation import CoordinateCalculation
from PlateCreator import PlateCreator
from configs import config as config

from configs.sign_config import type_signs_with_text, plate_for_signatures_with_text, codes_signs


class ErrorCorrector(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1200, 600)
        self.ChangerType = ChangerType()
        self.PlateCreator = PlateCreator()

        self.ChangerType.list_widget.itemClicked.connect(self.change_type)
        self.PlateCreator.list_widget.itemClicked.connect(self.set_type_plate)
        self.label = QLabel(self)

        self.label.resize(960, 540)
        self.files_geojson = glob.glob(rf'./errorData/*.geojson')
        self.files_geojson.sort(key=lambda f: int(f.split('\\')[1].split('.')[0]))

        self.files_img = glob.glob(rf'./errorData/*.jpg')
        self.files_img.sort(key=lambda f: int(f.split('\\')[1].split('.')[0]))
        self.current_index = 0
        self.pixmap = QPixmap(self.files_img[self.current_index])

        self.label.setPixmap(self.pixmap)
        self.label_t = QLabel('Тип:', self)
        self.label_t.setGeometry(1000, 35, 1000, 20)

        self.label_img_type = QLabel(self)
        self.img_type = QPixmap(rf"./sings/V1.1.png")

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

        self.label_progress = QLabel(f'№{self.current_index}/{len(self.files_img)}', self)
        self.label_progress.move(560, 500)

        self.button_next = QPushButton("Вперед", self)
        self.button_next.move(560, 540)
        self.button_next.clicked.connect(self.next)

        self.button_end = QPushButton("Закончить", self)
        self.button_end.move(1000, 540)
        self.button_end.clicked.connect(self.finish_correction)

        self.button_change_type = QPushButton("Изменить тип", self)
        self.button_change_type.move(1000, 55)
        self.button_change_type.clicked.connect(self.open_change_type_window)

        self.button_delete = QPushButton("Удалить", self)
        self.button_delete.move(1000, 150)
        self.button_delete.clicked.connect(self.delete_sign)

        self.button_create_plate = QPushButton("Создать табличку", self)
        self.button_create_plate.move(1000, 200)
        self.button_create_plate.clicked.connect(self.create_plate)

        self.label_img_type_plate = QLabel(self)
        self.img_type_plate = QPixmap()
        self.label_img_type_plate.setPixmap(self.img_type_plate)
        self.label_img_type_plate.resize(100, 100)
        self.label_img_type_plate.move(1000, 220)
        self.label_img_type_plate.hide()

        self.label_type_plate = QLabel('', self)
        self.label_type_plate.setGeometry(1105, 200, 1105, 20)

        self.button_delete_plate = QPushButton("Удалить табличку", self)
        self.button_delete_plate.move(1000, 300)
        self.button_delete_plate.clicked.connect(self.delete_plate)
        self.button_delete_plate.setEnabled(False)

        self.textbox_text_plate = QLineEdit(self)
        self.textbox_text_plate.move(1105, 220)
        self.textbox_text_plate.resize(80, 20)
        self.textbox_text_plate.setEnabled(False)

        self.set_data()
        self.setWindowTitle("Исправлять ошибки")

    def delete_plate(self):
        self.label_type_plate.setText("")
        self.img_type_plate = QPixmap("")
        self.label_img_type_plate.setPixmap(self.img_type_plate)
        self.textbox_text_plate.setText("")
        self.button_delete_plate.setEnabled(False)
        self.textbox_text_plate.setEnabled(False)
        self.label_img_type_plate.hide()
        os.remove(rf'./errorData/plates/{str(self.current_index)}.geojson')

    def create_plate(self):
        if self.PlateCreator.isVisible():
            self.PlateCreator.hide()
        else:
            self.PlateCreator.show()

    def delete_sign(self):
        with open(config.PATH_TO_GEOJSON, encoding='utf-8') as f:
            data = geojson.load(f)
        with open(self.files_geojson[self.current_index], encoding='utf-8') as f:
            id = geojson.load(f)['features'][0]["properties"]["id"]
        #TODO почему-то крашит прогу, а без этого работет
        #new_data = []
        #for feature in data:
        #    print(feature)
        #if feature["properties"]["id"] != id:
        #    pass
        #new_data.append(feature)
        #self.save_new_geojson(new_data)
        os.remove(self.files_geojson[self.current_index])
        os.remove(self.files_img[self.current_index])
        self.files_geojson.pop(self.current_index)
        self.files_img.pop(self.current_index)
        self.delete_plate()
        self.next()

    def finish_correction(self):
        user_futures = []
        with open(config.PATH_TO_GEOJSON, encoding='utf-8') as f:
            data = geojson.load(f)
        ids_elements = []
        for path in self.files_geojson:
            with open(path, encoding='utf-8') as f:
                user_future = geojson.load(f)['features'][0]
                user_futures.append(user_future)
                id = user_future["properties"]["id"]
                ids_elements.append(id)
        for index in range(len(data['features'])):
            feature = data['features'][index]
            if "id" in feature["properties"] and feature["properties"]["id"] in ids_elements:
                index_changed_element = ids_elements.index(feature["properties"]["id"])
                data['features'][index] = user_futures[index_changed_element]
        data['features'] += self.features_plate()
        self.save_new_geojson(data)

    def features_plate(self):
        features_plates = []
        for file_name in os.listdir("./errorData/plates"):
            path_to_file = os.path.join("./errorData/plates", file_name)
            with open(path_to_file, encoding='utf-8') as f:
                features_plates.append(geojson.load(f)["features"])
        return features_plates

    def save_new_geojson(self, new_geojson):
        with open(config.PATH_TO_GEOJSON, 'w') as f:
            dump(new_geojson, f)

    def change_type(self, item):
        type_of_sing = item.text().replace("V", "")
        self.label_type.setText(type_of_sing)
        self.img_type = QPixmap(rf"./sings/{item.text()}.png")
        self.label_img_type.setPixmap(self.img_type)
        self.textbox_text.setEnabled(type_of_sing in type_signs_with_text)
        self.ChangerType.hide()

    def set_type_plate(self, item):
        type_of_plate = item.text()
        self.label_type_plate.setText(type_of_plate)
        self.img_type_plate = QPixmap(rf"./sings/V{item.text()}.png")
        self.label_img_type_plate.setPixmap(self.img_type_plate)
        self.textbox_text_plate.setEnabled(item.text() in plate_for_signatures_with_text)
        self.button_delete_plate.setEnabled(True)
        self.label_img_type_plate.show()
        self.PlateCreator.hide()

    #TODO Не работает но нужно сделать, красибо
    #def set_pixmap(self, img, label):
    #    img_pix = QPixmap(img)
    #    self.label.setPixmap(img_pix)
    def open_change_type_window(self):
        if self.ChangerType.isVisible():
            self.ChangerType.hide()
        else:
            self.ChangerType.show()

    def next(self):
        self.create_feature_plate()
        self.change_geojson()
        if self.current_index == len(self.files_geojson) - 1:
            self.current_index = 0
        else:
            self.current_index += 1
        self.set_data()
        self.label_progress.setText(f'№{self.current_index}/{len(self.files_img)}')

    def prev(self):
        self.create_feature_plate()
        self.change_geojson()
        if self.current_index == 0:
            self.current_index = len(self.files_geojson) - 1
        else:
            self.current_index -= 1
        self.set_data()
        self.label_progress.setText(f'№{self.current_index}/{len(self.files_img)}')

    def set_data(self):
        self.feature = self.get_feature_object()
        self.pixmap = QPixmap(self.files_img[self.current_index])
        self.draw_box()
        self.label_type.setText(self.feature["properties"]['type'])
        self.img_type = QPixmap(rf"./sings/V{self.feature['properties']['type']}.png")
        self.label_img_type.setPixmap(self.img_type)
        self.toggle_textbox()
        self.checkbox_side.setChecked(self.feature["properties"]['side'] == "True")
        self.set_plate()

    def set_plate(self):
        path_to_plate = rf'./errorData/plates/{str(self.current_index)}.geojson'
        if os.path.isfile(path_to_plate):
            with open(path_to_plate, encoding='utf-8') as f:
                data = geojson.load(f)
            data = data['features']
            if "MVALUE" in data["properties"]:
                self.textbox_text_plate.setText(data["properties"]["MVALUE"])
            self.textbox_text_plate.setEnabled("MVALUE" in data["properties"])

            self.label_type_plate.setText(data["properties"]["type"])
            self.img_type_plate = QPixmap(rf"./sings/V{data['properties']['type']}.png")
            self.label_img_type_plate.setPixmap(self.img_type_plate)
            self.label_img_type_plate.show()
            self.button_delete_plate.setEnabled(True)
        else:
            if self.label_type_plate.text() != '':
                self.textbox_text_plate.setText("")
                self.textbox_text_plate.setEnabled(False)
                self.label_type_plate.setText("")
                self.button_delete_plate.setEnabled(False)
                self.label_img_type_plate.hide()

    def create_feature_plate(self):
        if self.label_type_plate.text() != "":
            coordinates = self.feature["geometry"]["coordinates"]
            azimuth = float(self.feature["properties"]["azimuth"])
            first_dot = list(CoordinateCalculation.calculate_prew_point(coordinates[0][0], coordinates[0][1], azimuth, index_round=6))
            second_dot = list(CoordinateCalculation.calculate_prew_point(coordinates[0][0], coordinates[0][1], azimuth, index_round=6))
            type_sing = self.label_type_plate.text()
            properties_plate = {"type": type_sing, "code": int(codes_signs[type_sing])}
            geometry_plate = {"type": "LineString", "coordinates":[first_dot, second_dot]}

            if self.textbox_text_plate.text() != "":
                properties_plate["MVALUE"] = self.textbox_text_plate.text()
                properties_plate["SEM250"] = self.textbox_text_plate.text()
            feature = Feature(geometry=geometry_plate, properties=properties_plate)

            feature_collection = FeatureCollection(feature)
            with open(rf'./errorData/plates/{str(self.current_index)}.geojson', 'w') as f:
                geojson.dump(feature_collection, f)


    def toggle_textbox(self):
        is_contain_text = self.feature["properties"]['type'] in type_signs_with_text
        self.textbox_text.setEnabled(is_contain_text)
        self.textbox_text.setText(self.feature["properties"]["MVALUE"] if is_contain_text else "")

    def draw_box(self):
        painter = QPainter(self.pixmap)
        painter.setPen(QPen(QColor(0, 0, 0), 2))  # Черный цвет, толщина 2 пикселя
        x = self.get_item_from_arr(self.feature["properties"]["pixel_coordinates_x"])
        y = self.get_item_from_arr(self.feature["properties"]["pixel_coordinates_y"])
        h = self.get_item_from_arr(self.feature["properties"]["h"])
        w = self.get_item_from_arr(self.feature["properties"]["w"])
        painter.drawRect(int(x / 2), int(y / 2), int(w / 2), int(h / 2))  # Рисуем квадрат
        painter.end()
        self.label.setPixmap(self.pixmap)

    def get_item_from_arr(self, array):
        if isinstance(array, list):
            return int(array[-3])
        else:
            return int(array.replace(" ", "")[1:-1].split(',')[-3])

    def get_feature_object(self):
        with open(self.files_geojson[self.current_index], encoding='utf-8') as f:
            data = geojson.load(f)
        return data['features'][0]

    def change_geojson(self):
        old_properties = self.feature["properties"].copy()
        self.feature["properties"]['type'] = self.label_type.text()
        self.feature["properties"]['side'] = str(self.checkbox_side.isChecked())

        if self.feature["properties"]['type'] in type_signs_with_text:
            self.feature["properties"]['MVALUE'] = self.textbox_text.text()
            self.feature["properties"]['SEM250'] = self.textbox_text.text()
        else:
            if 'MVALUE' in self.feature["properties"]:
                self.feature["properties"].pop("MVALUE")
                self.feature["properties"].pop("SEM250")
        if old_properties != self.feature["properties"]:
            features = [Feature(geometry=self.feature["geometry"], properties=self.feature["properties"])]
            feature_collection = FeatureCollection(features)
            with open(self.files_geojson[self.current_index], 'w', encoding='utf-8') as f:
                dump(feature_collection, f)
    def clean_corrector(self):

    def create_image_with_errors(self):
        result = []
        with open(config.PATH_TO_GEOJSON) as f:
            data = geojson.load(f)
        counter = 0

        for feature in data['features']:
            for item in feature["properties"]:
                features = []
                frame_number = self.get_item_from_arr(feature["properties"]['absolute_frame_numbers'])
                result.append(feature)
                #if item == 'MVALUE' and feature["properties"]['MVALUE'] == "":
                #    frame_number = float(feature["properties"]['num']) - 70
                #    result.append(feature)
                #if feature["properties"]['type'] == "5.8.1":
                #    frame_number = float(feature["properties"]['num']) - 70
                #    result.append(feature)
                #if feature["properties"]['type'] == "3.1" or feature["properties"]['type'] == "3.2":
                #    frame_number = float(feature["properties"]['num']) - 70
                #    result.append(feature)
                if frame_number != None:
                    features.append(Feature(geometry=feature["geometry"], properties=feature["properties"]))
                    feature_collection = FeatureCollection(features)

                    number_video = int(frame_number // 63600)
                    frame_number_for_save = int(frame_number % 63600)
                    files = os.listdir(config.PATH_TO_VIDEO)
                    new_path = os.path.join(config.PATH_TO_VIDEO, str(files[number_video]))
                    cap = cv2.VideoCapture(new_path)
                    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number_for_save)
                    ret, frame = cap.read()
                    while not ret:
                        ret, frame = cap.read()
                    frame = cv2.resize(frame, dsize=(960, 540))
                    #cv2.imshow("frame", frame)
                    cv2.imwrite(rf'./errorData/{str(counter)}.jpg', frame)
                    with open(rf'./errorData/{str(counter)}.geojson', 'w') as f:
                        dump(feature_collection, f)
                    counter += 1
                    break
