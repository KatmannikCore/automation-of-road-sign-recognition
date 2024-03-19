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
        self.is_turn_left = True
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
        self.is_turn_left = True
        self.turn_distance = 0
        self.frames = []
        self.segment_length = 0
        self.last_index_of_gps = 0

    def calculate_azimuth_change(self, old_azimuth, new_azimuth):
        azimuth_change = new_azimuth - old_azimuth
        if azimuth_change > 180:
            azimuth_change = azimuth_change - 360
        elif azimuth_change < -180:
            azimuth_change = azimuth_change + 360
        return azimuth_change

    def calculate_current_points(self):
        lat1, lon1 = self.coordinates[0]  #start_point
        lat2, lon2 = self.coordinates[-1] #end_point
        start_point = [lat1, lon1, self.azimuths[0] ]
        end_point   = [lat2, lon2, self.azimuths[-1]  ]
        x1, y1= self.Converter.coordinateConverter(lat1, lon1, "epsg:4326", "epsg:32635")
        x2, y2= self.Converter.coordinateConverter(lat2, lon2, "epsg:4326", "epsg:32635")
        p1 = Point2D(y1, x1)
        p2 = Point2D(y2, x2)
        line = ogz(point_a=p1, point_b=p2)
        length = line.length
        direction = line.direction
        azimuth_offset = 60
        if self.calculate_azimuth_change(self.azimuths[-1], self.azimuths[0]) < 0:
            azimuth_offset = -60

        revers_start_point = self.calculate_revers_dot(azimuth_offset, length, p1, direction)
        revers_end_point = self.calculate_revers_dot(azimuth_offset / 2, length, p1, direction)

        revers_start_point.append(self.azimuths[0])
        revers_end_point.append(self.azimuths[-1])
        return start_point, end_point, revers_start_point, revers_end_point
    def calculate_revers_dot(self, azimuth_offset, length, p1, direction):
        azimuth = direction + azimuth_offset
        line = Line2D(length=length, direction=azimuth)
        p2 = pgz(point=p1, line=line)
        x, y = self.Converter.coordinateConverter(p2.y, p2.x, "epsg:32635", "epsg:4326")
        return [x, y]

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
            self.signs[index].is_turn_left = self.is_turn_left
    def append_coordinates(self, item):
        if not self.coordinates:
            self.coordinates.append(self.Reader.get_current_coordinate(config.INDEX_OF_GPS))
            self.coordinates.append(item)
        else:
            if item != self.coordinates[-1]:
                self.coordinates.append(item)

    #def calculate_turn_distance(self):
    #    result_distance = 0
    #    for i in range(len(self.coordinates) - 1):
    #        result_distance += geodesic(self.coordinates[i], self.coordinates[i + 1]).meters
    #    return result_distance

   #def calculate_sign_distance_from_start_to_sign(self, sign):
   #    try:
   #        number = self.frames.index(sign.frame_numbers[-1])
   #        #result = (self.turn_distance / (len(self.frames)- 1)) * number
   #        return number
   #    except Exception as e:
   #        return 0
    def is_turn(self):
        # TODO Сделать чтобы не учитывала точки ближе метра

        delta = self.Reader.get_azimuth(config.INDEX_OF_GPS + 1) - self.Reader.get_azimuth(config.INDEX_OF_GPS)
        is_turn = abs(delta) > 10
        if is_turn:
            if delta < 0:
                self.is_turn_left = True

            else:
                self.is_turn_left = False
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
                sign.distance  = self.frames.index(sign.frame_numbers[-1])
            else:
                sign.distance  = -1
                return 2
            if (sign.distance / (self.segment_length)) >= 2:
                if not self.is_turn_left:
                    if  sign.pixel_coordinates_x[1] - sign.pixel_coordinates_x[-2] < 0:
                        return  7
                if coefficient_frames < 150:
                    return 5
                else:
                    return 8
            #TODO dangerous construction

            if sign.pixel_coordinates_x[1] - sign.pixel_coordinates_x[-2] > 0:
                if sign.is_turn_left:
                    return 8
                elif coefficient_frames > 250:
                    return 7
            elif not self.is_turn_left:
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
                    return 2#"out of categories"
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
            if int(item.number_turn) in self.signs_dict:
                self.signs_dict[int(item.number_turn)].append(item)
            else:
                self.signs_dict[int(item.number_turn)] = [item]
