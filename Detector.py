import random

import cv2
from tensorflow.keras.models import load_model
from skimage.color import rgb2gray
import numpy as np
import re
import easyocr
reader = easyocr.Reader(['ru'])

from Reader import Reader
model = load_model('./test_c171_r10_e80.h5')
model_krug = load_model('./models_200_10/krug.h5')
model_red = load_model('./models_100/red.h5')
model_blue = load_model('./models_200_10/blue.h5')
model_treugolnik = load_model('./models_200_10/treugolnik.h5')
model_servises = load_model('./models_200_10/servises.h5')
model_tabl_I = load_model('./models_200_10/tabl l.h5')
model_tabl__ = load_model('./models_200_10/tab.h5')
model_danger = load_model('./models_200_10/treugolnik/danger.h5')
model_pimicanie = load_model('./models_200_10/treugolnik/pimicanie.h5')
model_suzenie = load_model('./models_200_10/treugolnik/suzenie.h5')

name_signs_cnn = {
    "blue": ["4.1.4", "4.3","4.2.2", "4.1.6", "4.1.3", "4.1.1", "4.1.4", "0000010420", "4.2.1","4.1.2"],
    "krug": ["3.2", "3.24", "3.18.2", "3.13", "3.5", "3.4", "3.20.1",  "empty", "3.18.1", "3.9"],
    "red": ["2.5","3.1"],
    "treugolnik": ["1.21", "1.23", "1.29", "1.8", "1.17", "suzenie","1.32", "1.5", "pimicanie", "danger"],
    "servises": ["5.16", "7.1", "7.3", "7.5", "7.4", "7.11", "7.18", "7.2", "5.14.2", "7.15", "7.7", "6.12.2", "7.16"],
    "tablichka __" : ["8.12", "8.3.1",  "8.8", "8.10", "8.2.6", "8.2.1", "8.3.2", "8.5.7", "8.1.3", "7.14.1", "8.1.1", "8.15" ],
    "tablichka |": ["8.2.4", "8.2.3", "8.2.2"]
}
name_sub_signs_cnn = {
<<<<<<< HEAD
    "danger": ['1.11.2', '1.11.1', '1.12.2'],
    "pimicanie": ['2.3.3', '2.3.2', '2.3.1'],
    "suzenie":['1.20.2','1.20.3','1.20.2']
=======
    "suzenie": ['1.11.2', '1.11.1', '1.12.2'],
    "pimicanie": ['2.3.3', '2.3.2', '2.3.1'],
    "danger":['1.20.2','1.20.3','1.20.2']
>>>>>>> 998a996f7b9ff34b8162bd56787139ef7b4beec8
}

type_signs_yolo = {
    "parkovka": "6.4",
    "glavnaya doroga": "2.1",
    "peshehodnyj perehod": "5.16.2",
    "ostanovka i parkovka zapreshena": "3.27",
    "napravlenie dvizheniya po polosam" : "5.8.1",
    "ustupi dorogu" : "2.4",
    "zhilaya zona" : "5.38",
    "tupik" : "6.8.1",
    "polosa dlya obshestvennogo transporta" : "5.9.1",
    "konec odnostoronnego dvizheniya" : "5.6",
    "ostanovka avtobusa tablichka" : "5.16",
    "doroga s odnostoronnim dvizheniem" : "5.5",
    "napravlenie glavnoj dorogi" : "7.13.1",
    "Sbros vseh ogranicheniu" : "3.31",
    "viezd na dorogu s odnostorinnim dvizeniem >": "5.7.2",

    "nachalo nas punkta bel s dom" : "5.22.2",
    "konec nas punkta bel s dom" : "5.23.2",
    "nachalo nas punkta bel" : "5.22.1",
    "konec nas punkta bel" : "5.23.1",
    "nachalo nas punkta sin" : "5.23.3",
    "konec nas punkta sin" : "5.25.3"
}
class Detector:
    def __init__(self):
        self.Conf_threshold = 0.5
        self.NMS_threshold = 0.5

        self.COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0),
                  (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        net = cv2.dnn.readNet(r'D:\Urban\yolov4\darknet\build\darknet\\x64\backup\sings_full_best.weights', r'D:\Urban\yolov4\darknet\build\darknet\x64\sings_full.cfg')
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        self.class_name = []
        with open('classes.txt', 'r') as f:
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
            res = self.__find_sign(img, class_id, minImg)

            text_on_sign = self.text_handler(minImg, res, class_id)

            color = self.COLORS[int(class_id) % len(self.COLORS)]
            label = "%s : %f" % (self.class_name[class_id], score)

            item = [box, color, label, self.class_name[class_id], res, text_on_sign]
            result.append(item)
        return result
    def text_handler(self,minImg, res, class_id):
        type_signs_with_text = ['3.24', '3.11', '3.12', '3.13', '3.14', '3.15', '8.1.4', '8.1.3', '8.2.1', '8.2.2', '8.2.5', '8.2.6', '7.1.2', '7.7.1', '8.1.1', '7.9.1', '', '', '']
        name_signs_with_text = [ "nachalo nas punkta bel s dom", "konec nas punkta bel s dom", "nachalo nas punkta bel", "konec nas punkta bel", "nachalo nas punkta sin", "konec nas punkta sin"]
        result = ''
        if res in type_signs_with_text or self.class_name[class_id] in name_signs_with_text:
            result = self.read_text(minImg)
        if result == []:
            result = ''
        return result

    def read_text(self, minImg):
        result = reader.readtext(minImg)
        if len(result) != 0:
            # оставить только цифры
            result = re.sub(r'\D', '', result[0][1])
        return result
    def __get_minImg(self, box, frame):
        x, y, w, h = box
        x1 = x + w
        y1 = y + h
        minImg = frame[y:y1, x:x1]
        return minImg
    def __find_sign(self,img, class_id,  minImg):
        self.counter +=1
        if self.class_name[class_id] == "blue":
            number_result = np.argmax(model_blue.predict_step(np.expand_dims(img, axis=0)))
            result_type = name_signs_cnn["blue"][number_result]
        elif self.class_name[class_id] == "treugolnik":
            number_result = np.argmax(model_treugolnik.predict_step(np.expand_dims(img, axis=0)))
            result_type = name_signs_cnn["treugolnik"][number_result]
<<<<<<< HEAD

=======
>>>>>>> 998a996f7b9ff34b8162bd56787139ef7b4beec8
            if result_type == 'danger':
                number_result = np.argmax(model_danger.predict_step(np.expand_dims(img, axis=0)))
                result_type = name_sub_signs_cnn['danger'][number_result]
            elif result_type == 'pimicanie':
                number_result = np.argmax(model_pimicanie.predict_step(np.expand_dims(img, axis=0)))
                result_type = name_sub_signs_cnn['pimicanie'][number_result]
            elif result_type == 'suzenie':
                number_result = np.argmax(model_suzenie.predict_step(np.expand_dims(img, axis=0)))
                result_type = name_sub_signs_cnn['suzenie'][number_result]
<<<<<<< HEAD

=======
>>>>>>> 998a996f7b9ff34b8162bd56787139ef7b4beec8
        elif self.class_name[class_id] == "krug":
            number_result = np.argmax(model_krug.predict_step(np.expand_dims(img, axis=0)))
            result_type = name_signs_cnn["krug"][number_result]
        elif self.class_name[class_id] == "red":
            number_result = np.argmax(model_red.predict_step(np.expand_dims(img, axis=0)))
            result_type = name_signs_cnn["red"][number_result]
        elif self.class_name[class_id] == "servises":
            number_result = np.argmax(model_servises.predict_step(np.expand_dims(img, axis=0)))
            result_type = name_signs_cnn["servises"][number_result]
        elif self.class_name[class_id] == "tablichka __":
            number_result = np.argmax(model_tabl__.predict_step(np.expand_dims(img, axis=0)))
            result_type = name_signs_cnn["tablichka __"][number_result]
        elif self.class_name[class_id] == "tablichka |":
            number_result = np.argmax(model_tabl_I.predict_step(np.expand_dims(img, axis=0)))
            result_type = name_signs_cnn["tablichka |"][number_result]
        else:
            result_type = type_signs_yolo[self.class_name[class_id] ]
        if result_type == "":
            result_type = "empty"
        return result_type