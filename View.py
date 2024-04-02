#!/usr/bin/python
# -*- coding: cp1251 -*-
import cv2
import os
from geojson import Feature, FeatureCollection, dump, LineString
import config as config
from CoordinateCalculation import CoordinateCalculation
from Detector import Detector
from Reader import Reader
from Converter import Converter
from SignHandler import SignHandler
from Frame import Frame
from Turn import Turn
class View:
    def __init__(self):
        self.detector = Detector()
        self.classifier = [
            "parkovka",
            "treugolnik",
            "krug",
            "glavnaya doroga",
            "peshehodnyj perehod",
            "ostanovka i parkovka zapreshena",
            "viezd na dorogu s odnostorinnim dvizeniem >",
            "napravlenie dvizheniya po polosam",
            "ustupi dorogu",
            "red",
            "zhilaya zona",
            "tupik",
            "polosa dlya obshestvennogo transporta",
            "blue",
            "servises",
            "konec odnostoronnego dvizheniya",
            "tablichka |",
            "tablichka __",
            "ostanovka avtobusa tablichka",
            "doroga s odnostoronnim dvizheniem",
            "napravlenie glavnoj dorogi",
            "nachalo nas punkta bel s dom",
            "konec nas punkta bel s dom",
            "nachalo nas punkta bel",
            "konec nas punkta bel",
            "nachalo nas punkta sin",
            "konec nas punkta sin",
            "Sbros vseh ogranicheniu",
            "platnaua doroga"
        ]
        self.calculation = CoordinateCalculation()
        self.Converter = Converter()
        self.Reader = Reader(config.PATH_TO_GPX)
        for root, dirs, files in os.walk(config.PATH_TO_VIDEO):
            self.files = files
        self.cap = cv2.VideoCapture(config.PATH_TO_VIDEO + files[config.INDEX_OF_VIDEO])
        self.sign_handler = SignHandler()
        self.turn = Turn()
        for item in self.classifier:
            config.ClASSIFIER[item] = []

    def count_frames(self):
        for item in self.files:
            cap = cv2.VideoCapture(config.PATH_TO_VIDEO + item)
            config.COUNT_FRAMES += cap.get(cv2.CAP_PROP_FRAME_COUNT)

    def create_line(self, h, name_sing):
        x1, y1, x2, y2 = self.calculation.get_line(config.INDEX_OF_GPS, h)
        #Cоздание линии (2х точек) 
        line = LineString([(y1, x1), (y2, x2)])
        #создание объукта описывающего ДЗ
        feature = Feature(geometry=line, properties={"type": name_sing, "id": config.INDEX_OF_SING})
        config.FEATURES.append(feature)
        config.INDEX_OF_SING += 1

    def write_geoJson(self):
        #Создание объекта хронящего все ДЗ
        feature_collection = FeatureCollection(config.FEATURES)
        with open(config.PATH_TO_GEOJSON, 'w', encoding='cp1251') as f:
            dump(feature_collection, f, skipkeys=False, ensure_ascii=True)

    def switch_video(self):
        if self.cap.get(cv2.CAP_PROP_FRAME_COUNT) <= config.INDEX_OF_FRAME:
            if len(self.files) - 1 >= config.INDEX_OF_VIDEO + 1:
                config.INDEX_OF_VIDEO += 1
                self.cap = cv2.VideoCapture(config.PATH_TO_VIDEO + self.files[config.INDEX_OF_VIDEO])
                config.INDEX_OF_FRAME = 0
                return False
            else:
                self.write_geoJson()
                return True

    def draw_rectangles(self, frame):
        rectangles = self.detector.find_rectangles(frame)

        detections = []
        frame_for_checking = []
        for box, color, label, name_sign, number_sign, text_on_sign in rectangles:
            if name_sign != 'peshehodnyj perehod':
                x, y, w, h = box
                detections.append([x, y, w, h])

                x1, y1 = self.Reader.get_current_coordinate(config.INDEX_OF_GPS)
                x1, y1 = self.Converter.coordinateConverter(x1, y1,"epsg:4326", "epsg:32635")

                object_frame = Frame()
                object_frame.x = x
                object_frame.y = y
                object_frame.w = w
                object_frame.h = h
                object_frame.name_sign = name_sign
                object_frame.latitude = x1
                object_frame.longitude = y1
                object_frame.number_frame = config.COUNT_PROCESSED_FRAMES
                object_frame.number_sign = number_sign
                object_frame.text_on_sign = text_on_sign

                frame_for_checking.append(object_frame)

                cv2.rectangle(frame, box, color, 1)
                cv2.putText(frame, label, (box[0], box[1] - 10),
                           cv2.FONT_HERSHEY_COMPLEX, 0.5, color, 1)
        #if rectangles:
        if self.turn.is_turn():
            self.turn.append_azimuths(self.Reader.get_azimuth(config.INDEX_OF_GPS+1))
            self.turn.append_coordinates(self.Reader.get_current_coordinate(config.INDEX_OF_GPS+1))
            self.turn.last_index_of_gps = config.INDEX_OF_GPS
            self.turn.frames.append(config.COUNT_PROCESSED_FRAMES)
        if frame_for_checking:
            self.turn = self.sign_handler.check_the_data_to_add(frame_for_checking, self.turn)

        return rectangles
