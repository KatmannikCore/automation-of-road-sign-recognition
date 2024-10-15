import glob
import os

import cv2
import geojson
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtWidgets import QPushButton, QLabel, QWidget
from geojson import Feature, FeatureCollection

from PlateCreatorWidget import PlateCreatorWidget
from SignChangerWidget import SignChangerWidget
from configs import config as config
from configs.sign_config import type_signs_with_text

class ErrorCorrector(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1200, 600)
        self.setWindowTitle("Исправление ошибок")
        self.mainLayout = QtWidgets.QGridLayout()

        self.signCreator = SignChangerWidget()
        self.signCreator.button_delete.clicked.connect(self.delete_sign)

        self.plateCreator = PlateCreatorWidget()

        self.mainLayout.addWidget(self.signCreator, 0, 0)
        self.mainLayout.addWidget(self.plateCreator, 1, 0)

        self.setLayout(self.mainLayout)

        self.label = QLabel(self)
        self.label.resize(960, 540)
        self.pixmap = QPixmap()
        self.label.setPixmap(self.pixmap)


        self.files_geojson = glob.glob(rf'./errorData/*.geojson')
        self.files_geojson.sort(key=lambda f: int(f.split('\\')[1].split('.')[0]))

        self.files_img = glob.glob(rf'./errorData/*.jpg')
        self.files_img.sort(key=lambda f: int(f.split('\\')[1].split('.')[0]))
        self.current_index = 0

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

        self.setWindowTitle("Исправлять ошибки")

        self.set_data()

    def delete_sign(self):
        with open(config.PATH_TO_GEOJSON, encoding='utf-8') as f:
            data = geojson.load(f)
        with open(self.files_geojson[self.current_index], encoding='utf-8') as f:
            id = geojson.load(f)['features'][0]["properties"]["id"]

        os.remove(self.files_geojson[self.current_index])
        os.remove(self.files_img[self.current_index])
        self.files_geojson.pop(self.current_index)
        self.files_img.pop(self.current_index)
        self.plateCreator.delete_plate()
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
        with open(config.PATH_TO_GEOJSON, 'w', encoding="utf-8") as f:
            geojson.dump(new_geojson, f, ensure_ascii=False)

    def next(self):
        self.plateCreator.create_feature_plate(self.feature, self.current_index)
        self.change_geojson()
        if self.current_index == len(self.files_geojson) - 1:
            self.current_index = 0
        else:
            self.current_index += 1
        self.set_data()


    def prev(self):
        self.plateCreator.create_feature_plate(self.feature, self.current_index)
        self.change_geojson()
        if self.current_index == 0:
            self.current_index = len(self.files_geojson) - 1
        else:
            self.current_index -= 1
        self.set_data()


    def set_data(self):
        self.plateCreator.current_index = self.current_index
        self.signCreator.current_index = self.current_index
        self.feature = self.get_feature_object()
        self.pixmap = QPixmap(self.files_img[self.current_index])
        self.draw_box()
        self.signCreator.toggle_textbox(self.feature)
        self.signCreator.set_sing(self.feature)
        self.plateCreator.set_plate()
        self.label_progress.setText(f'№{self.current_index}/{len(self.files_img)}')

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
        self.feature["properties"]['type'] = self.signCreator.label_type.text()
        self.feature["properties"]['side'] = str(self.signCreator.checkbox_side.isChecked())

        if self.feature["properties"]['type'] in type_signs_with_text:
            self.feature["properties"]['MVALUE'] = self.signCreator.textbox_text.text()
            self.feature["properties"]['SEM250'] = self.signCreator.textbox_text.text()
        else:
            if 'MVALUE' in self.feature["properties"]:
                self.feature["properties"].pop("MVALUE")
                self.feature["properties"].pop("SEM250")
        if old_properties != self.feature["properties"]:
            features = [Feature(geometry=self.feature["geometry"], properties=self.feature["properties"])]
            feature_collection = FeatureCollection(features)
            with open(self.files_geojson[self.current_index], 'w', encoding='utf-8') as f:
                geojson.dump(feature_collection, f, ensure_ascii=False)

    def clean_corrector(self):
        self.delete_files("./errorData")
        self.delete_files("./errorData/plates")

    def delete_files(self, directory):
        """Удаляет все файлы .1.txt и .png в заданном каталоге, оставляя каталоги."""
        for root, folders, files in os.walk(directory):
            for file in files:
                if file.endswith(('.geojson', '.jpg')):
                    path_to_file = os.path.join(root, file)
                    try:
                        os.remove(path_to_file)
                    except OSError as e:
                        print(f"Ошибка при удалении {path_to_file}: {e}")

    def create_image_with_errors(self):
        result = []
        with open(config.PATH_TO_GEOJSON, encoding="utf-8") as f:
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
                    with open(rf'./errorData/{str(counter)}.geojson', 'w', encoding="utf-8") as f:
                        geojson.dump(feature_collection, f, ensure_ascii=False)
                    counter += 1
                    break
