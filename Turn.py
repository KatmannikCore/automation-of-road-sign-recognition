import config
from Reader import Reader

from pygeoguz.simplegeo import *
from pygeoguz.objects import *
from Converter import Converter
from geopy.distance import geodesic
class Turn:
    def __init__(self):
        self.signs = []
        self.signs_dict = {}
        self.Reader = Reader(config.PATH_TO_GPX)
        self.coordinates = []
        self.azimuths = []
        self.was_there_turn = False
        self.turn_directions = 'straight'
        self.turn_distance = 0
        self.frames = []
        self.segment_length = 0
        self.Converter = Converter()
        self.last_index_of_gps = 0
    def clean(self):
        self.signs = []
        self.signs_dict = {}
        self.coordinates = []
        self.azimuths = []
        self.was_there_turn = False
        self.turn_directions = 'straight'
        self.turn_distance = 0
        self.frames = []
        self.segment_length = 0
        self.last_index_of_gps = 0


    def append_azimuths(self, item):
        if not self.azimuths:
            self.azimuths.append(self.Reader.get_azimuth(config.INDEX_OF_GPS))
            self.azimuths.append(item)
        else:
            if item != self.azimuths[-1]:
                self.azimuths.append(item)
    def set_direction_signs(self):
        for index in range(len(self.signs)):
            self.signs[index].is_turn = True
            self.signs[index].turn_directions = self.turn_directions
    def append_coordinates(self, item):
        if not self.coordinates:
            self.coordinates.append(self.Reader.get_current_coordinate(config.INDEX_OF_GPS))
            self.coordinates.append(item)
        else:
            if item != self.coordinates[-1]:
                self.coordinates.append(item)

    def is_turn(self):
        # TODO Сделать чтобы не учитывала точки ближе метра
        delta = self.Reader.get_azimuth(config.INDEX_OF_GPS + 1) - self.Reader.get_azimuth(config.INDEX_OF_GPS)
        is_turn = abs(delta) > 10
        if is_turn:
            if delta < 0:
                self.turn_directions = 'left'
            else:
                self.turn_directions = 'right'
            self.was_there_turn = True
            return True
        else:
            return False

    def handle_turn(self):
        self.segment_length = len(self.frames) / 3
        for index in range(len(self.signs)):
            if len(self.signs[index].frame_numbers) > 3:
                self.signs[index].number = self.handle_sing(self.signs[index])

    def handle_sing(self, sign):
        max_size = self.calculation_max_size(sign)
        min_size = self.calculation_min_size(sign)
        coefficient_frames = self.calculation_coefficient_frames(sign, min_size, max_size)

        if self.calculation_different_x(sign) > 1000 and coefficient_frames > 150:
            return 7
        else:
            if sign.frame_numbers[-1] in self.frames:
                sign.distance = self.frames.index(sign.frame_numbers[-1])
            else:
                sign.distance = -1
                return 2
            if (sign.distance / round(self.segment_length, 0)) >= 2:
                if  self.turn_directions == 'right':
                    if sign.pixel_coordinates_x[1] - sign.pixel_coordinates_x[-2] < 0:
                        return 7
                if coefficient_frames < 150:
                    return 5
                else:
                    return 8
            # TODO dangerous construction

            if sign.pixel_coordinates_x[1] - sign.pixel_coordinates_x[-2] > 0:
                if sign.turn_directions == "left":
                    return 8
                elif coefficient_frames > 250:
                    return 7
            elif self.turn_directions == "right" and coefficient_frames > 150:
                return 7

            coefficient_size = self.calculation_coefficient_size(min_size, max_size)
            if coefficient_size < 5:
                return 5
            else:
                if coefficient_frames > 250:
                    return 2
                elif coefficient_frames < 150:
                    return 5
                else:
                    return 2  # "out of categories"
    def calculation_different_x(self, sing):
        return sing.pixel_coordinates_x[-2] - min(sing.pixel_coordinates_x)
    def calculation_max_size(self, sing):
        max_index = sing.w.index(max(sing.w))
        return sing.w[max_index] * sing.h[max_index]

    def calculation_min_size(self, sing):
        min_index = sing.w.index(min(sing.w))
        return sing.w[min_index] * sing.h[min_index]
    def calculation_coefficient_frames(self, sign, min_size, max_size):
        return round((max_size - min_size) / len(sign.frame_numbers),0)

    def calculation_coefficient_size(self, min_size, max_size):
        return round(max_size/min_size,1)

    def arr_to_dict(self):
        for item in self.signs:
            if int(item.azimuth) in self.signs_dict:
                self.signs_dict[int(item.azimuth)].append(item)
            else:
                self.signs_dict[int(item.azimuth)] = [item]

    def add_points(self):
        count_points = 3
        coordinate_offset = 2
        for index in range(count_points):
            index_of_gpx = self.last_index_of_gps + index + coordinate_offset
            self.append_coordinates( self.Reader.get_current_coordinate( index_of_gpx))
            self.append_azimuths(self.Reader.get_azimuth(index_of_gpx))
