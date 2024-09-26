import json
import time
from threading import Thread

import geojson

from Converter import Converter
from PyQt5.QtCore import QUrl
import cv2
from PyQt5.QtGui import QFont
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from qtpy import QtGui
from json import dump

import re

from SignHandler import SignHandler
from ViewTrack import ViewTrack
from configs import config
from Reader import Reader
from View import View
from CoordinateCalculation import CoordinateCalculation

from geojson import FeatureCollection, dump
import os
from geojson import Feature, LineString

from ErrorCorrector import ErrorCorrector


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.converter = Converter()

        self.calculation = None
        self.k = -0.5
        self.b = 10.9
        self.count_empty = 0
        self.counter_progress = 5000
        self.Reader = None
        self.is_wait = False
        self.is_brake = False
        self.msgBox = None
        self.setGeometry(0, 0, 1200, 600)
        self.view = None
        self.thread = Thread(target=self.treatment, daemon=True)
        self.ErrorCorrector = ErrorCorrector()
        self.ViewTrack = None

        self.create_player()
        self.create_text()
        self.create_buttons()
        #self.set_path_to_video()
        self.check_for_filling_of_data()

        self.show()

    def openErrorCorrector(self, checked):
        if self.ErrorCorrector.isVisible():
            self.ErrorCorrector.hide()
        else:
            self.ErrorCorrector.show()

    def create_player(self):
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

        self.label = QLabel(self)
        self.pixmap = QPixmap('../cnt.png')
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

        self.button_choose_dir = QPushButton("Open Directory", self)
        self.button_choose_dir.move(960, 30)
        self.button_choose_dir.clicked.connect(self.choose_dir)

        self.button_choose_GPX = QPushButton("open GPX", self)
        self.button_choose_GPX.move(960, 60)
        self.button_choose_GPX.clicked.connect(self.choose_GPX)

        self.button_choose_geojson = QPushButton("Выбрать geojson", self)
        self.button_choose_geojson.move(960, 90)
        self.button_choose_geojson.clicked.connect(self.choose_geojson)

        self.button_treatment = QPushButton("Начать обработку", self)
        self.button_treatment.move(960, 120)
        self.button_treatment.clicked.connect(self.start_processing)

       #self.button_open_save = QPushButton("open save", self)
       #self.button_open_save.move(960, 150)
       #self.button_open_save.clicked.connect(self.open_save)

       #self.button_save_as = QPushButton("save as", self)
       #self.button_save_as.move(960, 180)
       #self.button_save_as.clicked.connect(self.save)

        self.button_end = QPushButton("Законьчить", self)
        self.button_end.move(960, 210)
        self.button_end.clicked.connect(self.finish_processing)
        self.button_end.setEnabled(False)
        #self.speed_frame_box = QLineEdit(self)
        #self.speed_frame_box.move(960, 240)
        #self.speed_frame_box.setText(str(config.FRAME_STEP))

        #self.button_speed_frame = QPushButton("Выполнить", self)
        #self.button_speed_frame.move(960, 270)
        #self.button_speed_frame.clicked.connect(self.set_speed_frame)

        self.button_corrector = QPushButton("Корректировать ошибки", self)
        self.button_corrector.move(630, 540)
        self.button_corrector.clicked.connect(self.openErrorCorrector)

        self.button_viewTrack = QPushButton("viewTrack ", self)
        self.button_viewTrack.move(730, 540)
        self.button_viewTrack.clicked.connect(self.openViewTrack )

    def start_processing(self):
        self.set_default_values_configs()
        self.toggle_button_activity()
        self.is_brake = False
        self.thread.start()

    def toggle_button_activity(self):
        self.button_corrector.setEnabled(not self.button_corrector.isEnabled())
        self.button_viewTrack.setEnabled(not self.button_viewTrack.isEnabled())
        self.button_choose_dir.setEnabled(not self.button_choose_dir.isEnabled())
        self.button_choose_GPX.setEnabled(not self.button_choose_GPX.isEnabled())
        self.button_choose_geojson.setEnabled(not self.button_choose_geojson.isEnabled())
        self.button_treatment.setEnabled(not self.button_treatment.isEnabled())
        self.button_end.setEnabled(not self.button_end.isEnabled())
    def set_default_values_configs(self):
       config.VIDEOS = []
       config.FRAME_STEP = 5
       config.COUNT_PROCESSED_FRAMES = 0
       config.INDEX_OF_FRAME = 0
       config.INDEX_OF_VIDEO = 0
       config.INDEX_OF_All_FRAME = config.INDEX_OF_FRAME + (63600 * config.INDEX_OF_VIDEO)
       config.INDEX_OF_GPS = int(round(config.INDEX_OF_All_FRAME / 60, 0))
       config.INDEX_OF_SING = 0
    def openViewTrack(self):
        if self.ViewTrack.isVisible():
            self.ViewTrack.hide()
        else:
            self.ViewTrack.show()

    def check_for_filling_of_data(self):
        is_filled_all = len(config.PATH_TO_GEOJSON) > 3 and len(config.PATH_TO_GPX) > 3 and len(config.PATH_TO_VIDEO) > 3
        self.button_treatment.setEnabled(is_filled_all)
        self.button_corrector.setEnabled(is_filled_all)
        self.button_viewTrack.setEnabled(is_filled_all)
        if is_filled_all:
            self.ViewTrack = ViewTrack()

    def set_path_to_video(self):
        config.PATH_TO_GPX = r"D:\Urban\vid\test\07,07,20211.gpx"
        self.Reader = Reader(config.PATH_TO_GPX)
        self.label_gpx.setText("<font color=black>" + str(config.PATH_TO_GPX) + "</font>")

        config.PATH_TO_VIDEO = r"D:\Urban\vid\test\GOPR0064" + "\\"
        config.VIDEOS = os.listdir(config.PATH_TO_VIDEO)
        self.label_dir.setText("{}".format(config.PATH_TO_VIDEO))
        self.Files = os.listdir(config.PATH_TO_VIDEO)

        self.label_geojson.setText("{}".format(config.PATH_TO_GEOJSON))

    def set_speed_frame(self):
        speed_value = int(self.speed_frame_box.text())
        config.FRAME_STEP = speed_value
        self.speed_frame_box.setText(str(config.FRAME_STEP))

    def play(self):
        self.is_wait = not self.is_wait

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
            dump(json, f)
        QMessageBox.about(self, "Сообщение", "Сохранено")

    def treatment(self):

        self.calculation = CoordinateCalculation()
        self.view = View()
        self.view.count_frames()
        count_gpx = self.Reader.get_count_dot()
        start_time = time.time()

        while self.view.cap.isOpened():
            if self.is_brake:
                break
            speed = self.Reader.get_speed(config.INDEX_OF_GPS)
            config.FRAME_STEP = round(self.k * speed + self.b, 0)
            ret, frame = self.view.cap.read()
            if ret:
                if config.INDEX_OF_All_FRAME + 100 > config.COUNT_FRAMES:
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    print('Elapsed time: ', elapsed_time / 60)
                    self.final_data_processing()
                    break
                self.label.setPixmap(self.convert_cv_qt(frame))
                config.COUNT_PROCESSED_FRAMES += 1
                if round(speed, 0) != 0:
                    retangles = self.view.draw_rectangles(frame)
                    self.label.setPixmap(self.convert_cv_qt(frame))
                    if not retangles:
                        self.count_empty += 1
                    else:
                        self.count_empty = 0
               # cv2.waitKey(1)
            self.switch_frame()
            if self.view.switch_video():
                break
            #cv2.waitKey(1)
            while self.is_wait:
                pass
        #except Exception as e:
        #    print("error", e)
        #    print('frame', config.INDEX_OF_FRAME)
        print("end")
    def switch_frame(self):
        config.INDEX_OF_FRAME += config.FRAME_STEP
        config.INDEX_OF_All_FRAME += config.FRAME_STEP

        count_frame_for_gps = config.INDEX_OF_All_FRAME - (config.INDEX_OF_GPS * 60)
        if count_frame_for_gps > 60:
            config.INDEX_OF_GPS += 1
        self.view.cap.set(cv2.CAP_PROP_POS_FRAMES, config.INDEX_OF_FRAME)
    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(960, 540, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def choose_GPX(self):
        gpx_path = QtWidgets.QFileDialog.getOpenFileName(filter="gpx (*.gpx)")

        config.PATH_TO_GPX = gpx_path[0].replace('/', '\\')
        if config.PATH_TO_GPX == "":
            self.label_gpx.setText("<font color=black>" + "Пустой GPX" + "</font>")
        else:
            self.Reader = Reader(config.PATH_TO_GPX)
            self.label_gpx.setText("<font color=black>" + str(config.PATH_TO_GPX) + "</font>")
        self.check_for_filling_of_data()

    def choose_dir(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        config.PATH_TO_VIDEO = dirlist.replace('/', '\\') + "\\"
        config.VIDEOS = os.listdir(config.PATH_TO_VIDEO)

        self.label_dir.setText("{}".format(config.PATH_TO_VIDEO))
        self.Files = dirlist
        self.check_for_filling_of_data()

    def choose_geojson(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        save_path, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                   "geojson (*.geojson)", options=options)
        save_path += '.geojson'
        config.PATH_TO_GEOJSON = save_path
        self.label_geojson.setText("{}".format(config.PATH_TO_GEOJSON))
        self.check_for_filling_of_data()

    #TODO Вынести в отельный класс
    # TODO handling_signs и handling_side объеденить в один метод

    def handling_signs(self):
        grouped_objects = {}
        features = []
        # Обработка результатов знаков

        for obj in self.view.sign_handler.result_signs:
            key = str(obj.car_coordinates_x[-1]) + str(obj.is_left)
            grouped_objects.setdefault(key, []).append(obj)
        for key, items in grouped_objects.items():
            coefficient = 2
            for item in items:
                x1, y1, x2, y2 = self.calculation.get_line(item, coefficient)
                coefficient += 1

                feature = self.calculation.create_feature_object(x1, x2, y1, y2, item)
                features.append(feature)
        return features

    def handling_side(self):
        grouped_objects = {}
        features = []
        for obj in self.view.sign_handler.side_signs:
            key = str(obj.car_coordinates_x[-1]) + str(obj.is_left)
            grouped_objects.setdefault(key, []).append(obj)
        for key, items in grouped_objects.items():
            coefficient = 2
            for item in items:
                x1, y1, x2, y2 = self.calculation.get_line(item, coefficient)
                coefficient += 1
                item.azimuth = (item.azimuth + 90) % 360
                feature = self.calculation.create_feature_object(x1, x2, y1, y2, item)
                features.append(feature)
        return features

    def handling_turns(self):
        features = []
        # Обработка поворотов
        for turn in self.view.sign_handler.turns:
            [start_point, end_point, revers_start_point, revers_end_point] = self.calculation.calculation_four_dots(
                turn)

            temp_obj = {
                "0": start_point, "1": start_point, "2": start_point,
                "3": revers_end_point, "4": revers_end_point, "5": revers_start_point,
                "5.1": revers_start_point, "6": revers_start_point,
                "7": revers_end_point, "8": revers_end_point
            }
            grouped_objects = {}
            for obj in turn.signs:
                key = str(obj.number)
                grouped_objects.setdefault(key, []).append(obj)

            for key, items in grouped_objects.items():
                x_current, y_current, x_prev, y_prev, azimuth = temp_obj[key]
                x_current, y_current = self.converter.coordinateConverter(x_current, y_current, "epsg:4326",
                                                                          "epsg:32635")
                x_prev, y_prev = self.converter.coordinateConverter(x_prev, y_prev, "epsg:4326", "epsg:32635")

                coefficient = 2
                for item in items:
                    item.azimuth = azimuth
                    x1, y1, x2, y2 = self.calculation.calculate_result_line(item, coefficient,
                                                                            x_prev, y_prev,
                                                                            x_current, y_current)
                    x1, y1 = self.converter.coordinateConverter(x1, y1, "epsg:32635", "epsg:4326")
                    x2, y2 = self.converter.coordinateConverter(x2, y2, "epsg:32635", "epsg:4326")
                    coefficient += 1
                    feature = self.calculation.create_feature_object(x1, x2, y1, y2, item)
                    features.append(feature)
        return features
    def finish_processing(self):

        self.toggle_button_activity()
        self.save_result()
        self.create_image_with_errors()
        self.view.cap.release()
        self.is_brake = True
        self.thread.join()
        self.thread = Thread(target=self.treatment, daemon=True)
        #cv2.destroyAllWindows()

       #self.stop_progressing()

    def save_result(self):
        path = config.PATH_TO_GEOJSON

        features_signs = self.handling_signs()
        features_turns = self.handling_turns()
        features_side = self.handling_side()
        features = features_signs + features_turns + features_side
        signs_for_delete = []
        for i in range(len(features)):
            item_for_matching = features[i]
            for j in range(len(features)):
                item_with_which_matching = features[j]

                item_with_x = item_with_which_matching["properties"]['w']
                item_with_x = [int(re.findall(r'\b\d+\b', item)[0]) for item in item_with_x.split(',')]
                average_item_with_x = sum(item_with_x) / len(item_with_x)
                item_for_x = item_for_matching["properties"]['w']
                item_for_x = [int(re.findall(r'\b\d+\b', item)[0]) for item in item_for_x.split(',')]
                average_item_for_x = sum(item_for_x) / len(item_for_x)

                item_for_car_x = item_for_matching["properties"]['car_coordinates_x']
                item_for_car_x = [float(re.findall(r'\b\d+\b', item)[0]) for item in item_for_car_x.split(',')]
                item_for_car_y = item_for_matching["properties"]['car_coordinates_y']
                item_for_car_y = [float(re.findall(r'\b\d+\b', item)[0]) for item in item_for_car_y.split(',')]
                item_with_car_x = item_with_which_matching["properties"]['car_coordinates_x']
                item_with_car_x = [float(re.findall(r'\b\d+\b', item)[0]) for item in item_with_car_x.split(',')]
                item_with_car_y = item_with_which_matching["properties"]['car_coordinates_y']
                item_with_car_y = [float(re.findall(r'\b\d+\b', item)[0]) for item in item_with_car_y.split(',')]

                if "del" not in features[i]:
                    if average_item_for_x != average_item_with_x:
                        if item_for_matching["properties"]["left"] == item_with_which_matching["properties"]["left"]:
                            if item_for_matching["properties"]["type"] == item_with_which_matching["properties"][
                                "type"]:
                                distance = self.calculation.calculation_distance(item_for_car_x[-1],
                                                                                 item_for_car_y[-1],
                                                                                 item_with_car_x[-1],
                                                                                 item_with_car_y[-1])
                                if distance < 20:
                                    item_for_azimuth = float(item_for_matching["properties"]["azimuth"])
                                    item_with_azimuth = float(item_with_which_matching["properties"]["azimuth"])
                                    difference_azimuth = abs(
                                        self.calculation.calculate_azimuth_change(item_for_azimuth, item_with_azimuth))
                                    if difference_azimuth < 30:
                                        features[j]["del"] = 0
                                        if int(features[j]["properties"]["length"]) > int(
                                                features[i]["properties"]["length"]):
                                            signs_for_delete.append(item_for_matching)
                                        else:
                                            signs_for_delete.append(item_with_which_matching)
                                        break
            #TODO Непонятно зачем но крашит программу
            #for item in signs_for_delete:
            #    print(item)
            #    features.remove(item)
        feature_collection = FeatureCollection(features)

        with open(path, 'w', encoding='cp1251') as f:
            dump(feature_collection, f, skipkeys=False, ensure_ascii=True)
        print("save")

    def create_image_with_errors(self):
        result = []
        with open(config.PATH_TO_GEOJSON) as f:
            data = geojson.load(f)
        counter = 0

        for feature in data['features']:
            for item in feature["properties"]:
                features = []
                frame_number = self.ErrorCorrector.get_item_from_arr(feature["properties"]['absolute_frame_numbers'])
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
                    print(feature["properties"])

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
