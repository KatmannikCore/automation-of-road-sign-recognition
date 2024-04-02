from collections import Counter
import numpy as np
import math
from Converter import Converter
class Sign:
    def __init__(self):
        #TODO убрать повторение коорднинат
        self.converter = Converter()
        self.pixel_coordinates_x = []
        self.pixel_coordinates_y = []
        self.h = []
        self.w = []
        self.result_yolo = []
        self.car_coordinates_x = []
        self.car_coordinates_y = []
        self.frame_numbers = []
        self.result_CNN = []
        self.deletion_counter = 0
        self.is_left = False
        self.azimuth = None

        self.is_turn = False
        self.turn_directions = 'straight'
        self.text_on_sign = []

        self.distance = 0
        self.number = 0
    def get_azimuth(self):
        return self.azimuth
    def __str__(self):
        x, y = self.converter.coordinateConverter(self.car_coordinates_x[-1],self.car_coordinates_y[-1],  "epsg:32635", "epsg:4326")
        return f"is_left: {self.is_left}\n" \
               f"x: {self.pixel_coordinates_x},\n" \
               f"y: {self.pixel_coordinates_y},\n" \
               f"h: {self.h},\n" \
               f"w: {self.w},\n" \
               f"name1: {self.get_the_most_often(self.result_yolo)},\n" \
               f"name2: {self.result_CNN},\n" \
               f"frame: {self.frame_numbers}\n" \
               f"coordinate: {x}, {y}  \n"
    def json(self):
        json_object = {
            "name_one": self.get_the_most_often(self.result_yolo),
            "name_two": self.get_the_most_often(self.result_CNN),
            "w": self.w ,
            "h": self.h ,
            "x": self.pixel_coordinates_x,
            "y": self.pixel_coordinates_y,
            "length": int(len(self.frame_numbers))
        }
        return json_object
    def replace_car_coordinates(self, turn):
        self.car_coordinates_x = []
        self.car_coordinates_y = []
        for x, y in turn.coordinates:
            x, y = self.converter.coordinateConverter(x, y,"epsg:4326", "epsg:32635")
            self.car_coordinates_x.append(x)
            self.car_coordinates_y.append(y)
    def append_data(self, sign):
        self.pixel_coordinates_x.append(sign.x)
        self.pixel_coordinates_y.append(sign.y)
        self.h.append(sign.h)
        self.w.append(sign.w)
        self.result_yolo.append(sign.name_sign)
        self.set_car_coordinate(sign.latitude, sign.longitude)
        self.frame_numbers.append(sign.number_frame)
        self.result_CNN.append(sign.number_sign)
        if sign.text_on_sign != "":
            self.text_on_sign.append(sign.text_on_sign)

    def concat_two_object(self, sign):
        #for index in range(len(sign.h)):
        self.pixel_coordinates_x += sign.pixel_coordinates_x
        self.pixel_coordinates_y += sign.pixel_coordinates_y
        self.h += sign.h
        self.w += sign.w
        self.result_yolo += sign.result_yolo
        self.frame_numbers += sign.frame_numbers
        self.result_CNN += sign.result_CNN
        self.text_on_sign += sign.text_on_sign
        self.__append_car_coordinates(sign)
    def __append_car_coordinates(self, sign):
        self.car_coordinates_x += sign.car_coordinates_x
        self.car_coordinates_y += sign.car_coordinates_y
    def set_car_coordinate(self, x, y):
        if len(self.car_coordinates_x) == 0:
            self.car_coordinates_x.append(x)
            self.car_coordinates_y.append(y)
        else:
            if x != self.car_coordinates_x[-1]:
                self.car_coordinates_x.append(x)
                self.car_coordinates_y.append(y)

    def get_the_most_often(self, arr):
        if arr:
            return Counter(arr).most_common(1)[0][0]
        else:
            return ''

    def is_sign_on_edge_of_screen(self):
        half_screen_width = 960
        screen_width = 1920
        part_of_screen_width = 96
        part_of_screen_height = 96
        #TODO возможно part_of_screen_width ненужен

        if (screen_width - self.pixel_coordinates_x[-1]) < half_screen_width:
            check_width = (self.pixel_coordinates_x[-1] + self.w[-1] + part_of_screen_width) > screen_width
        else:
            check_width = (self.pixel_coordinates_x[-1] - self.w[-1] - part_of_screen_width) < 0

        check_height = (self.pixel_coordinates_y[-1] - self.h[-1] - part_of_screen_height) < 0

        return check_width or check_height