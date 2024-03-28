import math
from Reader import Reader
from Converter import Converter
import config as config

from geojson import Feature, LineString
class CoordinateCalculation:
    __one_radian = 57.2958
    def __init__(self):
        self.converter = Converter()
        self.reader = Reader(config.PATH_TO_GPX)

    def get_line(self, sign, coefficient):
        x1, y1, x2, y2 = self.__calculate_coordinates_sign_moving_straight(sign,coefficient)

        x1, y1 = self.converter.coordinateConverter(x1, y1,  "epsg:32635", "epsg:4326")
        x2, y2 = self.converter.coordinateConverter(x2, y2, "epsg:32635", "epsg:4326")
        return x1, y1, x2, y2


    def __get_current_coordinates_for_moving_straight(self,sign):
        return sign.car_coordinates_x[-1], sign.car_coordinates_y[-1]

    def __get_prev_coordinates_for_moving_straight(self,sign):
        return sign.car_coordinates_x[-2], sign.car_coordinates_y[-2]

    def __calculate_coordinates_sign_moving_straight(self, sign,coefficient):
        x_current, y_current = self.__get_current_coordinates_for_moving_straight(sign)
        x_prev, y_prev  = self.converter.coordinateConverter(x_current, y_current, "epsg:32635", "epsg:4326")
        az = (sign.azimuth + 180 ) % 360
        x_prev, y_prev = self.calculate_prew_point(x_prev, y_prev, az)
        x_prev, y_prev = self.converter.coordinateConverter(x_prev, y_prev, "epsg:4326", "epsg:32635")
        x1, y1, x2, y2 = self.calculate_result_line(sign, coefficient, x_current, y_current,x_prev, y_prev)
        return x1, y1, x2, y2


    @staticmethod
    def calculate_result_line(sign, coefficient, x_current, y_current, x_prev, y_prev):
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
    def calculate_prew_point(self, lat, lon, az):
        # Дистанция между точками в метрах
        distance = 5
        # Радиус Земли в метрах
        earth_radius = 6371000
        # Координаты первой точки
        lat1 = math.radians(lat)  # широта в радианах
        lon1 = math.radians(lon)  # долгота в радианах
        # Азимут в градусах
        azimuth = math.radians(az)
        # Вычисление координат второй точки
        lat_result = math.asin(math.sin(lat1) * math.cos(distance / earth_radius) + math.cos(lat1) * math.sin(
            distance / earth_radius) * math.cos(azimuth))
        lon_result = lon1 + math.atan2(math.sin(azimuth) * math.sin(distance / earth_radius) * math.cos(lat1),
                                 math.cos(distance / earth_radius) - math.sin(lat1) * math.sin(lat_result))
        # Переводим координаты обратно в градусы
        lat_result = math.degrees(lat_result)
        lon_result = math.degrees(lon_result)

        return lat_result, lon_result

    def distance_on_earth(self, lat1, lon1, lat2, lon2):
        R = 6371  # Радиус Земли в километрах
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        a = (math.sin(d_lat / 2) ** 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * (
                    math.sin(d_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return round(distance * 1000, 3)

    def create_feature_object(self, x1, x2, y1, y2, sign):
        line = LineString([(y1, x1), (y2, x2)])
        text_on_sign = sign.get_the_most_often(sign.text_on_sign)
        type = sign.get_the_most_often(sign.result_CNN)
        if text_on_sign != 0:
            feature = Feature(geometry=line, properties={
                "type": f"{type}",
                "MVALUE": f"{text_on_sign}",
                "SEM250": f"{text_on_sign}"
            })
        else:
            feature = Feature(geometry=line, properties={"type": f"{type}" })
        return feature
