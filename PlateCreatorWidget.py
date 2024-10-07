import os

import geojson
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
from geojson import Feature, FeatureCollection

from ModalWindowPlate import ModalWindowPlate
from configs.sign_config import plate_for_signatures_with_text, codes_signs
from CoordinateCalculation import CoordinateCalculation

class PlateCreatorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.button_create_plate = QPushButton("Создать табличку", self)
        self.button_create_plate.move(1000, 0)
        self.modalWindowPlate = ModalWindowPlate()
        self.button_create_plate.clicked.connect(self.create_plate)
        self.modalWindowPlate.list_widget.itemClicked.connect(self.set_type_plate)

        self.label_img_type_plate = QLabel(self)
        self.img_type_plate = QPixmap()
        self.label_img_type_plate.setPixmap(self.img_type_plate)
        self.label_img_type_plate.resize(100, 100)
        self.label_img_type_plate.move(1000, 20)
        self.label_img_type_plate.hide()

        self.label_type_plate = QLabel('', self)
        self.label_type_plate.setGeometry(1105, 0, 1105, 20)

        self.button_delete_plate = QPushButton("Удалить табличку", self)
        self.button_delete_plate.move(1000, 100)
        self.button_delete_plate.clicked.connect(self.delete_plate)
        self.button_delete_plate.setEnabled(False)

        self.textbox_text_plate = QLineEdit(self)
        self.textbox_text_plate.move(1105, 20)
        self.textbox_text_plate.resize(80, 20)
        self.textbox_text_plate.setEnabled(False)
        self.current_index = 0

    def clean(self):
        if self.label_type_plate.text() != '':
            self.textbox_text_plate.setText("")
            self.textbox_text_plate.setEnabled(False)
            self.label_type_plate.setText("")
            self.button_delete_plate.setEnabled(False)
            self.label_img_type_plate.hide()

    def create_plate(self):
        if self.modalWindowPlate.isVisible():
            self.modalWindowPlate.hide()
        else:
            self.modalWindowPlate.show()

    def delete_plate(self):
        self.label_type_plate.setText("")
        self.img_type_plate = QPixmap("")
        self.label_img_type_plate.setPixmap(self.img_type_plate)
        self.textbox_text_plate.setText("")
        self.button_delete_plate.setEnabled(False)
        self.textbox_text_plate.setEnabled(False)
        self.label_img_type_plate.hide()
        if os.path.exists(rf'./errorData/plates/{str(self.current_index)}.geojson'):
            os.remove(rf'./errorData/plates/{str(self.current_index)}.geojson')

    def set_type_plate(self, item):
        type_of_plate = item.text()
        self.label_type_plate.setText(type_of_plate)
        self.img_type_plate = QPixmap(rf"./sings/V{item.text()}.png")
        self.label_img_type_plate.setPixmap(self.img_type_plate)
        self.textbox_text_plate.setEnabled(item.text() in plate_for_signatures_with_text)
        self.button_delete_plate.setEnabled(True)
        self.label_img_type_plate.show()
        self.modalWindowPlate.hide()

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
            self.clean()

    def create_feature_plate(self, feature, number_file):
        if self.label_type_plate.text() != "":
            coordinates = feature["geometry"]["coordinates"]
            azimuth = float(feature["properties"]["azimuth"])
            first_dot = list(CoordinateCalculation.calculate_prew_point(coordinates[0][0], coordinates[0][1], azimuth,
                                                                        index_round=6))
            second_dot = list(CoordinateCalculation.calculate_prew_point(coordinates[0][0], coordinates[0][1], azimuth,
                                                                         index_round=6))
            type_sing = self.label_type_plate.text()
            properties_plate = {"type": type_sing, "code": int(codes_signs[type_sing])}
            geometry_plate = {"type": "LineString", "coordinates": [first_dot, second_dot]}

            if self.textbox_text_plate.text() != "":
                properties_plate["MVALUE"] = self.textbox_text_plate.text()
                properties_plate["SEM250"] = self.textbox_text_plate.text()
            feature = Feature(geometry=geometry_plate, properties=properties_plate)

            feature_collection = FeatureCollection(feature)
            with open(rf'./errorData/plates/{str(number_file)}.geojson', 'w', encoding="utf-8") as f:
                geojson.dump(feature_collection, f, ensure_ascii=False)