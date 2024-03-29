#!/usr/bin/python
# -*- coding: cp1251 -*-
import cv2
import os
from geojson import Point, Feature, FeatureCollection, dump, LineString
import json
import config as config
from CoordinateCalculation import CoordinateCalculation
from Detector import Detector
import random
from Reader import Reader
from Converter import Converter
from SignHandler import SignHandler
from Frame import Frame

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
        for item in self.classifier:
            config.ClASSIFIER[item] = []

    def count_frames(self):
        for item in self.files:
            cap = cv2.VideoCapture(config.PATH_TO_VIDEO + item)
            config.COUNT_FRAMES += cap.get(cv2.CAP_PROP_FRAME_COUNT)

    def create_line(self, h, name_sing):
        x1, y1, x2, y2 = self.calculation.get_line(config.INDEX_OF_GPS, h)
        #C������� ����� (2� �����) 
        line = LineString([(y1, x1), (y2, x2)])
        #�������� ������� ������������ ��
        feature = Feature(geometry=line, properties={"type": name_sing, "id": config.INDEX_OF_SING})
        config.FEATURES.append(feature)

        config.INDEX_OF_SING += 1
        #with open('data.txt', 'w') as fw:
        #    json.dump(config.ClASSIFIER, fw)

    def write_geoJson(self):
        #�������� ������� ��������� ��� ��
        feature_collection = FeatureCollection(config.FEATURES)
        with open(config.PATH_TO_GEOJSON, 'w', encoding='cp1251') as f:
            dump(feature_collection, f, skipkeys=False, ensure_ascii=True)

    def switch_video(self):
        if self.cap.get(cv2.CAP_PROP_FRAME_COUNT) <= config.INDEX_OF_FRAME:
            if len(self.files) - 1 >= config.INDEX_OF_VIDEO + 1:
                config.INDEX_OF_VIDEO += 1
                print(config.PATH_TO_VIDEO + self.files[config.INDEX_OF_VIDEO])
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
        for box, color, label, name_sign, number_sign in rectangles:
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
            frame_for_checking.append(object_frame)#([x, y, w, h, name_sign,  x1, y1, config.COUNT_PROCESSED_FRAMES, number_sign])

            cv2.rectangle(frame, box, color, 1)
            cv2.putText(frame, label, (box[0], box[1] - 10),
                       cv2.FONT_HERSHEY_COMPLEX, 0.5, color, 1)

        if frame_for_checking:
            self.sign_handler.check_the_data_to_add(frame_for_checking)
        return rectangles