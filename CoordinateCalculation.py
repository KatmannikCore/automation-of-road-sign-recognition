import math
from Reader import Reader
from Converter import Converter
import config as config

class CoordinateCalculation:
    __one_radian = 57.2958
    def __init__(self):
        self.converter = Converter()
        self.reader = Reader(config.PATH_TO_GPX)

    def get_line(self, sign, coefficient):
        feature_collection = []


        #delta_x, delta_y = CoordinateCalculation.__normalize_distance(delta_x, delta_y)
        x1, y1, x2, y2 = CoordinateCalculation.__calculate_sign_coordinates(sign, coefficient)

        x1, y1 = self.converter.coordinateConverter(x1, y1,  "epsg:32635", "epsg:4326")
        x2, y2 = self.converter.coordinateConverter(x2, y2, "epsg:32635", "epsg:4326")
        return x1, y1, x2, y2

    @staticmethod
    def __calculate_sign_coordinates(self,sign, coefficient):
        if sign.is_turn:
            if sign.is_turn_left:
                return self.__calculate_coordinates_sign_left_turn()
            else:
                return self.__calculate_coordinates_sign_right_turn()
        else:
            return self.calculate_coordinates_sign_moving_straight(sign,coefficient)

    @staticmethod
    def __get_current_coordinates_for_moving_straight(sign):
        return sign.car_coordinates_x[-1], sign.car_coordinates_y[-1]
    @staticmethod
    def __get_prev_coordinates_for_moving_straight(sign):
        return sign.car_coordinates_x[-2], sign.car_coordinates_y[-2]
    @staticmethod
    def __calculate_coordinates_sign_moving_straight(self, sign,coefficient):
        x_current, y_current = self.__get_current_coordinates_for_moving_straight(sign)
        #TODO Ошибка если у занака только одна пара координат
        #if len(sign.car_coordinates_x) == 1:
        #    return x_current, y_current
        x_prev, y_prev = self.__get_prev_coordinates_for_moving_straight(sign)
        x1, y1, x2, y2 = self.__calculate_result_line_for_moving_straight(sign, coefficient, x_current, y_current,x_prev, y_prev)
        return x1, y1, x2, y2

    @staticmethod
    def __calculate_result_line_for_moving_straight(self, sign, coefficient, x_current, y_current,x_prev, y_prev):
        delta_x = x_current - x_prev
        delta_y = y_current - y_prev
        if sign.is_left:
            if coefficient == 2:
                x2 = x_current
                y2 = y_current
            else:
                x2 = x_current - delta_y * (coefficient - 2)
                y2 = y_current + delta_x * (coefficient - 2)
            x1 = x_current - delta_y * (coefficient - 1)
            y1 = y_current + delta_x * (coefficient - 1)
        else:
            x1 = x_current + delta_y * coefficient
            y1 = y_current - delta_x * coefficient
            x2 = x_current + delta_y * (coefficient + 1)
            y2 = y_current - delta_x * (coefficient + 1)
        return x1, y1, x2, y2
    @staticmethod
    def __calculate_coordinates_sign_left_turn(self):
        pass

    @staticmethod
    def __calculate_coordinates_sign_right_turn(self):
        pass

    @staticmethod
    def __calculate_center_turn(self, start_point, end_point):
        # Находим координаты центра квадрата
        center_x = (start_point[0] + end_point[0]) / 2
        center_y = (start_point[1] + end_point[1]) / 2

        # Вычисляем разницу по x и y между центром и одной из вершин
        delta_x = start_point[0] - center_x
        delta_y = start_point[1] - center_y

        # Находим координаты  вершины квадрата
        x1, y1 = (center_x - delta_y, center_y + delta_x)
        x2, y2 = end_point
        midpoint_x = (x1 + x2) / 2
        midpoint_y = (y1 + y2) / 2
        return midpoint_x, midpoint_y

    def distance_on_earth(self, lat1, lon1, lat2, lon2):
        R = 6371  # Радиус Земли в километрах
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        a = (math.sin(d_lat / 2) ** 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * (
                    math.sin(d_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return round(distance * 1000, 3)