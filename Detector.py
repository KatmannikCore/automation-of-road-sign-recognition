#! /usr/bin/env python
# -*- coding: utf-8 -*-
import random

import cv2

from skimage.color import rgb2gray
import numpy as np
import re
import easyocr
reader = easyocr.Reader(['be'])
import difflib
from configs.sign_config import *

class Detector:
    def __init__(self):
        self.Conf_threshold = 0.5
        self.NMS_threshold = 0.5
        self.city_names = []
        self.COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0),
                  (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        net = cv2.dnn.readNet(r'./static/Yolov4/sings_full_best.weights', r'./static/Yolov4/sings_full.cfg')
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        self.class_name = []
        with open(r'./static/classes.txt', 'r') as f:
            self.class_name = [cname.strip() for cname in f.readlines()]
        self.model = cv2.dnn_DetectionModel(net)
        self.model.setInputParams(size=(416, 416), scale=1 / 255, swapRB=True)
        self.counter = 0
    def find_rectangles(self, frame):
        classes, scores, boxes = self.model.detect(frame, self.Conf_threshold, self.NMS_threshold)

        result = []
        for (class_id, score, box) in zip(classes, scores, boxes):
            minImg = self.__get_minImg(box, frame)

            img = cv2.resize(minImg, dsize=(28, 28))
            img = rgb2gray(img)
            res = self.__find_sign(img, class_id)

            text_on_sign = self.text_handler(minImg, res, class_id)

            color = self.COLORS[int(class_id) % len(self.COLORS)]
            label = "%s : %f" % (self.class_name[class_id], score)

            item = [box, color, label, self.class_name[class_id], res, text_on_sign]
            result.append(item)
        return result

    def remove_all_chars(self,input_string):
        return ''.join(char for char in input_string if char.isalnum())
    def find_similar_word(self, word, word_list):
        matches = difflib.get_close_matches(word, word_list)
        return matches
    def text_handler(self,minImg, res, class_id):

        text = ''
        if res in type_signs_with_text:
            text =  re.sub(r'\D', '', self.read_text(minImg))
        if self.class_name[class_id] in name_signs_city:
            text = self.read_text(minImg)
            text = self.remove_all_chars(text).lower()
            if self.city_names:
                text = difflib.get_close_matches(text, self.city_names)
            else:
                with open(r'D:\Urban\yolov4\yolov4-opencv-python/static/cities_be.txt', 'r', encoding='utf-8') as file:
                    # Читаем строки из файла и помещаем их в массив
                    lines = file.readlines()
                for line in lines:
                    self.city_names.append(line.replace('\n', '').lower())
                text = difflib.get_close_matches(text, self.city_names)
                pass
        if not text:
            return ""
        return text

    def read_text(self, minImg):
        result = reader.readtext(minImg)
        if len(result) == 0:
            return ""
            # оставить только цифры
            # result = re.sub(r'\D', '', result[0][1])
        return result[0][1]
    def __get_minImg(self, box, frame):
        x, y, w, h = box
        x1 = x + w
        y1 = y + h
        minImg = frame[y:y1, x:x1]
        return minImg

    def __find_sign(self, img, class_id):
        # Увеличиваем счетчик
        self.counter += 1
        # Инициализация переменной результата
        result_type = ""
        # Проверяем, есть ли модель для данного класса
        if self.class_name[class_id] in model_dict:
            model = model_dict[self.class_name[class_id]]
            number_result = np.argmax(model.predict_step(np.expand_dims(img, axis=0)))
            # Обработка особых случаев для класса "treugolnik"
            if self.class_name[class_id] == "treugolnik":
                result_type = name_signs_cnn["treugolnik"][number_result]
                if result_type in sub_models:
                    sub_model = sub_models[result_type]
                    number_result = np.argmax(sub_model.predict_step(np.expand_dims(img, axis=0)))
                    result_type = name_sub_signs_cnn[result_type][number_result]
            else:
                result_type = name_signs_cnn[self.class_name[class_id]][number_result]
        else:
            # Возвращаем тип из YOLO, если модели не найдены
            result_type = type_signs_yolo[self.class_name[class_id]]

        # Если результат пустой, присваиваем "empty"
        if result_type == "":
            result_type = "empty"

        return result_type