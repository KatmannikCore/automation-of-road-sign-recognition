import os
import re
import uuid
from json import dump
from geojson import FeatureCollection, LineString, Feature
from Converter import Converter
from CoordinateCalculation import CoordinateCalculation
from configs import config
from configs.sign_config import name_signs_city, type_signs_with_text, codes_signs


class FinalHandler:
    def __init__(self):
        self.calculation = CoordinateCalculation()
        self.converter = Converter()

    def save_result(self, result_signs, side_signs, turns):
        path = config.PATH_TO_GEOJSON
        features_signs = self.handling_signs(result_signs)
        features_turns = self.handling_turns(turns)
        features_side = self.handling_side(side_signs)
        features = features_signs + features_turns + features_side
        signs_for_delete = []
        for i in range(len(features)):
            item_for_matching = features[i]
            for j in range(len(features)):
                item_with_which_matching = features[j]

                item_with_x = item_with_which_matching["properties"]['w']
                item_with_x = [int(re.findall(r'\b\d+\b', item)[0]) for item in item_with_x.split(',')]
                average_item_with_x = sum(item_with_x) / len(item_with_x)
                item_for_x = item_for_matching["properties"]['w']
                item_for_x = [int(re.findall(r'\b\d+\b', item)[0]) for item in item_for_x.split(',')]
                average_item_for_x = sum(item_for_x) / len(item_for_x)

                item_for_car_x = item_for_matching["properties"]['car_coordinates_x']
                item_for_car_x = [float(re.findall(r'\b\d+\b', item)[0]) for item in item_for_car_x.split(',')]
                item_for_car_y = item_for_matching["properties"]['car_coordinates_y']
                item_for_car_y = [float(re.findall(r'\b\d+\b', item)[0]) for item in item_for_car_y.split(',')]
                item_with_car_x = item_with_which_matching["properties"]['car_coordinates_x']
                item_with_car_x = [float(re.findall(r'\b\d+\b', item)[0]) for item in item_with_car_x.split(',')]
                item_with_car_y = item_with_which_matching["properties"]['car_coordinates_y']
                item_with_car_y = [float(re.findall(r'\b\d+\b', item)[0]) for item in item_with_car_y.split(',')]

                if "del" not in features[i]:
                    if average_item_for_x != average_item_with_x:
                        if item_for_matching["properties"]["left"] == item_with_which_matching["properties"]["left"]:
                            if item_for_matching["properties"]["type"] == item_with_which_matching["properties"]["type"]:
                                distance = self.calculation.calculation_distance(item_for_car_x[-1], item_for_car_y[-1], item_with_car_x[-1], item_with_car_y[-1])
                                if distance < 20:
                                    item_for_azimuth = float(item_for_matching["properties"]["azimuth"])
                                    item_with_azimuth = float(item_with_which_matching["properties"]["azimuth"])
                                    difference_azimuth = abs(
                                        self.calculation.calculate_azimuth_change(item_for_azimuth, item_with_azimuth))
                                    if difference_azimuth < 30:
                                        features[j]["del"] = 0
                                        if int(features[j]["properties"]["length"]) > int(
                                                features[i]["properties"]["length"]):
                                            signs_for_delete.append(item_for_matching)
                                        else:
                                            signs_for_delete.append(item_with_which_matching)
                                        break
            # TODO Непонятно зачем но крашит программу
            # for item in signs_for_delete:
            #    print(item)
            #    features.remove(item)
        feature_collection = FeatureCollection(features)

        with open(config.PATH_TO_GEOJSON, 'w', encoding='cp1251') as f:
            dump(feature_collection, f, skipkeys=False, ensure_ascii=True)
        print("save")

    # TODO handling_signs и handling_side объеденить в один метод
    def handling_signs(self, arr_signs):
        grouped_objects = {}
        features = []
        for obj in arr_signs:
            key = str(obj.car_coordinates_x[-1]) + str(obj.is_left)
            grouped_objects.setdefault(key, []).append(obj)
        for key, items in grouped_objects.items():
            coefficient = 2
            for item in items:
                x1, y1, x2, y2 = self.calculation.get_line(item, coefficient)
                coefficient += 1
                feature = self.create_feature_object(x1, x2, y1, y2, item)
                features.append(feature)
        return features

    def handling_side(self, arr_signs):
        grouped_objects = {}
        features = []
        for obj in arr_signs:
            key = str(obj.car_coordinates_x[-1]) + str(obj.is_left)
            grouped_objects.setdefault(key, []).append(obj)
        for key, items in grouped_objects.items():
            coefficient = 2
            for item in items:
                x1, y1, x2, y2 = self.calculation.get_line(item, coefficient)
                coefficient += 1
                item.azimuth = (item.azimuth + 90) % 360
                feature = self.create_feature_object(x1, x2, y1, y2, item)
                features.append(feature)
        return features

    def handling_turns(self, arr_turns):
        features = []
        # Обработка поворотов
        for turn in arr_turns:
            [start_point, end_point, revers_start_point, revers_end_point] = self.calculation.calculation_four_dots(
                turn)

            temp_obj = {
                "0": start_point, "1": start_point, "2": start_point,
                "3": revers_end_point, "4": revers_end_point, "5": revers_start_point,
                "5.1": revers_start_point, "6": revers_start_point,
                "7": revers_end_point, "8": revers_end_point
            }
            grouped_objects = {}
            for obj in turn.signs:
                key = str(obj.number)
                grouped_objects.setdefault(key, []).append(obj)

            for key, items in grouped_objects.items():
                x_current, y_current, x_prev, y_prev, azimuth = temp_obj[key]
                x_current, y_current = self.converter.coordinateConverter(x_current, y_current, "epsg:4326",
                                                                          "epsg:32635")
                x_prev, y_prev = self.converter.coordinateConverter(x_prev, y_prev, "epsg:4326", "epsg:32635")

                coefficient = 2
                for item in items:
                    item.azimuth = azimuth
                    x1, y1, x2, y2 = self.calculation.calculate_result_line(item, coefficient,
                                                                            x_prev, y_prev,
                                                                            x_current, y_current)
                    x1, y1 = self.converter.coordinateConverter(x1, y1, "epsg:32635", "epsg:4326")
                    x2, y2 = self.converter.coordinateConverter(x2, y2, "epsg:32635", "epsg:4326")
                    coefficient += 1
                    feature = self.create_feature_object(x1, x2, y1, y2, item)
                    features.append(feature)
        return features

    def create_feature_object(self, x1, x2, y1, y2, sign):
        average_number_frame = sum(sign.absolute_frame_numbers) / len(sign.absolute_frame_numbers)
        number_video = int(average_number_frame // 63600)
        frame_number = int(average_number_frame % 63600)
        name_video = os.listdir(config.PATH_TO_VIDEO)[number_video]
        minute = frame_number // 3600
        seconds = (frame_number // 60) % 60
        time = f"{minute}:{seconds}"
        line = LineString([(y1, x1), (y2, x2)])
        if sign.get_the_most_often(sign.result_yolo)["name"] in name_signs_city:
            text_on_sign = sign.get_name_city()
        else:
            # TODO если табличка и город
            # TODO игнарировать если очень разные знаки или мало одинаковых совпадений
            if len(sign.text_on_sign) <= 4:
                text_on_sign = ""
            else:
                text_on_sign = sign.get_the_most_often(sign.text_on_sign)['name']
        type_sing = sign.get_the_most_often(sign.result_CNN)['name']

        properties_general = {
                "type": f"{type_sing}",
                "length": f"{len(sign.w)}",
                "side": f"{sign.is_sign_side}",
                "turn": f"{sign.turn_directions}",
                "left": f"{sign.is_left}",
                "num": f"{sign.number_sign}",
                "pixel_coordinates_x": f"{sign.pixel_coordinates_x}",
                "pixel_coordinates_y": f"{sign.pixel_coordinates_y}",
                "h": f"{sign.h}",
                "w": f"{sign.w}",
                "car_coordinates_x": f"{sign.car_coordinates_x}",
                "car_coordinates_y": f"{sign.car_coordinates_y}",
                "frame_numbers": f"{sign.frame_numbers}",
                "absolute_frame_numbers": f"{sign.absolute_frame_numbers}",
                "azimuth": f"{sign.azimuth}",
                "id": f"{uuid.uuid4()}",
                "time": time,
                "name_video": name_video,
                "code": int(codes_signs[type_sing])
            }
        properties_for_signs_with_text = {"MVALUE": f"{text_on_sign}", "SEM250": f"{text_on_sign}"}

        properties_general.update(properties_for_signs_with_text) if type_sing in type_signs_with_text  else properties_general

        feature = Feature(geometry=line, properties=properties_general)
        return feature