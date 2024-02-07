from collections import Counter
from geopy.distance import geodesic
from math import atan2, degrees, radians
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
        self.text_on_sign = []

        self.distance = 0
        self.number_turn = 0
        self.number_turn_start = 0
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

   #def calculate_azimuth(self):
   #    lat1, lon1 = radians(self.car_coordinates_x[-1]), radians(self.car_coordinates_y[-1])
   #    lat2, lon2 = radians(self.car_coordinates_x[-2]), radians(self.car_coordinates_y[-2])

   #    d_lon = lon2 - lon1

   #    y = math.sin(d_lon) * math.cos(lat2)
   #    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)
   #    bearing = atan2(y, x)
   #    self.azimuth = (degrees(bearing) + 360) % 360

    def append_data(self, sign):
        self.pixel_coordinates_x.append(sign.x)
        self.pixel_coordinates_y.append(sign.y)
        self.h.append(sign.h)
        self.w.append(sign.w)
        self.result_yolo.append(sign.name_sign)
        self.set_car_coordinate(sign.latitude, sign.longitude)
        self.frame_numbers.append(sign.number_frame)
        self.result_CNN.append(sign.number_sign)
        self.text_on_sign.append(sign.text_on_sign)


    def concat_two_object(self, sign):
        for index in range(len(sign.h)):
            self.pixel_coordinates_x.append(sign.pixel_coordinates_x[index])
            self.pixel_coordinates_y.append(sign.pixel_coordinates_y[index])
            self.h.append(sign.h[index])
            self.w.append(sign.w[index])
            self.result_yolo.append(sign.result_yolo[index])
            self.frame_numbers.append(sign.frame_numbers[index])
            self.result_CNN.append(sign.result_CNN[index])
            self.text_on_sign.append(sign.text_on_sign[index])
        self.__append_car_coordinates(sign)
    def __append_car_coordinates(self, sign):
        for index in range(len(sign.car_coordinates_x)):
            self.car_coordinates_x.append(sign.car_coordinates_x[index])
            self.car_coordinates_y.append(sign.car_coordinates_y[index])
    def set_car_coordinate(self, x, y):
        if len(self.car_coordinates_x) == 0:
            self.car_coordinates_x.append(x)
            self.car_coordinates_y.append(y)
        else:
            if x != self.car_coordinates_x[-1]:
                self.car_coordinates_x.append(x)
                self.car_coordinates_y.append(y)

    def get_the_most_often(self, arr):
        return Counter(arr).most_common(1)[0][0]

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