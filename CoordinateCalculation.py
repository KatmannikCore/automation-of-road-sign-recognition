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
        x_current = sign.car_coordinates_x[-1]
        y_current = sign.car_coordinates_y[-1]
        #TODO Ошибка если у занака только одна пара координат
        #if len(sign.car_coordinates_x) == 1:
        #    return x_current, y_current
        x_prev = sign.car_coordinates_x[-2]
        y_prev = sign.car_coordinates_y[-2]
        delta_x = x_current - x_prev
        delta_y = y_current - y_prev

        #delta_x, delta_y = CoordinateCalculation.__normalize_distance(delta_x, delta_y)
        x1, y1, x2, y2 = CoordinateCalculation.__calculate_sign_coordinates(sign, x_current, y_current, delta_x, delta_y, coefficient)

        x1, y1 = self.converter.coordinateConverter(x1, y1,  "epsg:32635", "epsg:4326")
        x2, y2 = self.converter.coordinateConverter(x2, y2, "epsg:32635", "epsg:4326")
        return x1, y1, x2, y2

    @staticmethod
    def __calculate_sign_coordinates(sign, x_current, y_current, delta_x, delta_y, coefficient):
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

    def distance_on_earth(self, lat1, lon1, lat2, lon2):
        R = 6371  # Радиус Земли в километрах
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        a = (math.sin(d_lat / 2) ** 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * (
                    math.sin(d_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return round(distance * 1000, 3)