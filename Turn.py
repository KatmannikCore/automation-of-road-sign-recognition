import config
from Reader import Reader

from geopy.distance import geodesic
class Turn:
    def __init__(self):
        self.signs = []
        self.signs_dict = {}
        self.Reader = Reader(config.PATH_TO_GPX)
        self.coordinates = []
        self.azimuths = []
        self.was_there_turn = False
        self.is_turn_left = True
        self.turn_distance = 0
        self.frames = []
    def append_azimuths(self, item):
        if not self.azimuths:
            self.azimuths.append(self.Reader.get_azimuth(config.INDEX_OF_GPS))
            self.azimuths.append(item)
        else:
            if item != self.azimuths[-1]:
                self.azimuths.append(item)

    def append_coordinates(self, item):
        if not self.coordinates:
            self.coordinates.append(item)
        else:
            if item != self.coordinates[-1]:
                self.coordinates.append(item)

    def calculate_turn_distance(self):
        result_distance = 0
        for i in range(len(self.coordinates) - 1):
            result_distance += geodesic(self.coordinates[i], self.coordinates[i + 1]).meters
        return result_distance

    def calculate_sign_distance_from_start_to_sign(self, sign):
        try:
            number = self.frames.index(sign.frame_numbers[-1])
            #result = (self.turn_distance / (len(self.frames)- 1)) * number
            return number
        except Exception as e:
            return 0
    def is_turn(self):
        # TODO Сделать чтобы не учитывала точки ближе метра

        delta = self.Reader.get_azimuth(config.INDEX_OF_GPS + 1) - self.Reader.get_azimuth(config.INDEX_OF_GPS)
        is_turn = abs(delta) > 10
        if is_turn:
            if delta < 0:
                self.is_turn_left = True
                # print("Лево")
            else:
                self.is_turn_left = False
            self.was_there_turn = True
            return True
        else:
            print("Прямо", end='\r')
            return False

    def handle_turn(self):
        for index in range(len(self.signs)):
            self.signs[index].number = self.handle_sing(self.signs[index])
            try:
                self.signs[index].distance  = self.frames.index(self.signs[index].frame_numbers[-1])
            except Exception as e:
                self.signs[index].distance  = 0
    def handle_sing(self, sign):

        if self.calculation_different_x(sign) > 1500:
            return 7
        if sign.pixel_coordinates_x[1] - sign.pixel_coordinates_x[-2] > 0:
            return 8
        else:
            max_size = self.calculation_max_size(sign)
            min_size = self.calculation_min_size(sign)
            coefficient_size = self.calculation_coefficient_size(min_size, max_size)
            if coefficient_size < 3:
                return 5.1
            else:
                coefficient_frames = self.calculation_coefficient_frames(sign, min_size, max_size)
                if coefficient_frames > 250:
                    return 3
                elif coefficient_frames < 150:
                    return 5
                else:
                    return "out of categories"
    def calculation_different_x(self, sing):
        return sing.pixel_coordinates_x[-1] - sing.pixel_coordinates_x[0]
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
            if int(item.number_turn) in self.signs_dict:
                self.signs_dict[int(item.number_turn)].append(item)
            else:
                self.signs_dict[int(item.number_turn)] = [item]
