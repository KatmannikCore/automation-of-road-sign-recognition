from Frame import Frame
from configs import config
from Reader import Reader
from Sign import Sign
from itertools import groupby
import copy
from Converter import Converter
from geopy.distance import geodesic
from configs.sign_config import names_signs_for_side
import matplotlib.pyplot as plt
class SignHandler:
    __number_for_incorrect_evidences = 9999.99
    __screen_width = 1920
    __half_screen_width = __screen_width / 3
    __difference_frames_for_remove_sign = 5
    __difference_frames_for_move_sign = 5
    __frame_gap_between_sign = 5
    __min_length_sign = 4

    def __init__(self):
        self.Reader = Reader(config.PATH_TO_GPX)
        self.signs = []
        self.result_signs = []
        self.side_signs = []
        self.turns = []
        self.was_there_turn = False
        self.turn_directions = 'straight'
        self.Converter = Converter()
        self.azimuth = 0

    def check_the_data_to_add(self, frame, Turn):
        # time.sleep(0.5)
        if frame:
            current_frame_number = frame[0].frame_number
            # Если знаков вообще нету
            if not self.signs:
                for sign in frame:
                    self.__add_sign(sign)
            else:

                if Turn.was_there_turn and not Turn.is_turn():
                    Turn = self.handling_turn_after_end(Turn, current_frame_number)
                frame = self.clean_frame_from_double_signs(frame)
                evidences = self.__check_pixel_coordinates(frame)
                evidences = self.__remove_collisions(evidences)
                frame_sign_to_add = self.__combine_frame_data_with_signs(evidences, frame)
                frame = self.__clean_frame(frame, frame_sign_to_add, evidences)
                self.__add_new_unknown_element(frame, frame_sign_to_add)

            self.set_azimuth_for_signs(current_frame_number)
            self.__remove_incorrect_signs(current_frame_number)
            if not Turn.is_turn():
                self.__move_final_signs(current_frame_number)
            else:
                if len(Turn.signs) == 0:
                    self.__move_final_signs(current_frame_number)
                Turn.signs = self.signs
            return Turn
    def set_azimuth_for_signs(self,current_frame_number):
        for index in range(len(self.signs)):
            if self.signs[index].frame_numbers[-1] == current_frame_number:
                self.signs[index].azimuth = self.Reader.get_azimuth(config.INDEX_OF_GPS + 1)
    def clean_frame_from_double_signs(self,frame):
        dict_frame = {}
        for item in frame:
            if item.name_sign in dict_frame:
                dict_frame[item.name_sign].append(item)
            else:
                dict_frame[item.name_sign] = [item]
        arr_frame = []
        for key in dict_frame:
            if len(dict_frame[key]) == 2:
                arr_frame.append(dict_frame[key])
        for item in arr_frame:
            square1 = item[0].x, item[0].y, item[0].w, item[0].h
            square2 = item[1].x, item[1].y, item[1].w, item[1].h
            if Frame.overlap_area(square2, square1) > 10:
                frame.remove(item[0])
        return frame
    def handling_turn_after_end(self, Turn, current_frame_number):
        if Turn.signs:  # Is there a turn sign?
            if len(Turn.coordinates) >= 2:
                Turn.add_points()
                self.__remove_incorrect_signs(current_frame_number)
                self.signs, Turn.signs = self.separation_signs(Turn)
                Turn.set_direction_signs()
                Turn.handle_turn()

                # TODO должен быть перенос коротких знаков
                self.turns.append(copy.copy(Turn))
        Turn.clean()
        return Turn

    def separation_signs(self, Turn):
        straight_signs = []
        turn_signs = []
        for item in self.signs:
            # TODO 7 Заменить на __min_length_sign result_CNN на get_the_most_often
            if len(item.result_CNN) >= 7 and item.frame_numbers[-1] < Turn.frames[-1]:
                turn_signs.append(item)
            else:
                item.replace_car_coordinates(Turn)
                straight_signs.append(item)
        return straight_signs, turn_signs

    def __clean_frame(self, frame, frame_sign_to_add, evidences):
        not_added_signs = self.get_not_added_signs(frame, frame_sign_to_add)
        items_for_remove = []
        for index in range(len(evidences)):
            for item in not_added_signs:
                if self.signs[index].get_the_most_often(self.signs[index].result_yolo)['name'] == item.name_sign:
                    vec = self.calculation_length_vector(item, index)
                    if abs(vec - (evidences[index][1])) <= 30 and vec != 0:
                        self.signs[index].append_data(item)
                        items_for_remove.append(item)
        new_frame = []
        for item in frame:
            if item not in items_for_remove:
                new_frame.append(item)
        frame = new_frame
        return frame
    def calculation_length_vector(self, item, index):
        delta_x = item.x - self.signs[index].pixel_coordinates_x[-1]
        delta_y = item.y - self.signs[index].pixel_coordinates_y[-1]
        # Теорема пифагора
        return round((delta_x ** 2 + delta_y ** 2) ** 0.5, 0)
    def get_not_added_signs(self,frame, frame_sign_to_add):
        result = []
        for item in frame:
            if item not in frame_sign_to_add:
                result.append(item)
        return result
    def __add_sign(self, sign):
        new_sign = Sign()
        new_sign.append_data(sign)
        self.signs.append(new_sign)

    def __remove_collisions(self, evidences):
        for i in range(len(evidences)):
            for j in range(len(evidences)):
                if i != j and evidences[i][0] == evidences[j][0]:
                    if evidences[i][1] < evidences[j][1]:
                        evidences[j][1] = SignHandler.__number_for_incorrect_evidences
                    else:
                        evidences[i][1] = SignHandler.__number_for_incorrect_evidences
        return evidences

    def __combine_frame_data_with_signs(self, evidences, frame):
        result = []
        for index in range(len(evidences)):
            if evidences[index][1] != SignHandler.__number_for_incorrect_evidences:
                if frame[0].frame_number - self.signs[index].frame_numbers[-1] < 7:
                    self.signs[index].append_data(frame[evidences[index][0]])
                    self.signs[index].number_sign = config.INDEX_OF_All_FRAME
                    result.append(frame[evidences[index][0]])
        return result

    def __calculation_distance(self, lat1, lon1, lat2, lon2):
        lat1, lon1 = self.Converter.coordinateConverter(lat1, lon1, "epsg:32635", "epsg:4326")
        lat2, lon2 = self.Converter.coordinateConverter(lat2, lon2, "epsg:32635", "epsg:4326")

        return geodesic((lat1, lon1), (lat2, lon2)).meters  # math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)

    def check_presence_of_nearby_sign(self, sign):
        for index in range(len(self.result_signs)):
            item = self.result_signs[index]
            average_item = sum(item.pixel_coordinates_x) / len(item.pixel_coordinates_x)
            average_sign = sum(sign.pixel_coordinates_x) / len(sign.pixel_coordinates_x)
            if average_sign != average_item:
                if item.is_left == sign.is_left:
                    if item.get_the_most_often(item.result_CNN)['name'] == sign.get_the_most_often(sign.result_CNN)[
                        'name']:
                        distance = self.__calculation_distance(sign.car_coordinates_x[-1], sign.car_coordinates_y[-1],
                                                               item.car_coordinates_x[-1], item.car_coordinates_y[-1])
                        if distance < 20:
                            self.result_signs[index].concat_two_object(sign)
                            return False
        return True


    def __move_final_signs(self, current_frame_number):
        signs_for_delete = []
        for index in range(len(self.signs)):
            if self.turns and self.signs[index].frame_numbers[-1] == self.turns[-1].frames[-1]:
                signs_for_delete.append(self.signs[index])
                self.signs[index].number = 8
                self.turns[-1].signs.append(self.signs[index])
            else:
                different_frame = current_frame_number
                frame_for_sign = self.signs[index].frame_numbers[
                                     -1] + SignHandler.__difference_frames_for_move_sign  # + 20 #+ 10
                # Проверка на коректность добовления добовляемого знака через:
                # 1)Изменение высоны расположения 2) Длинна объеиа 3) Разнать текущего номера кадра и последнего зафиксированного для знака
                if (#self.signs[index].is_sign_on_edge_of_screen() and
                        self.signs[index].get_the_most_often(self.signs[index].result_CNN)[
                            'count'] >= self.__min_length_sign):
                    if frame_for_sign < different_frame:
                        difference_in_screen_width_x_sign = SignHandler.__screen_width - self.signs[index].w[-1]
                        difference_in_screen_width_and_last_character_position = SignHandler.__screen_width - \
                                                                                 self.signs[index].pixel_coordinates_x[
                                                                                     -1]
                        # Проверка 2х знаков на принадлежность к одной и тойже части экрана
                        if len(self.signs[index].result_yolo) == 1:
                            self.signs[index].is_left = (
                                                                    difference_in_screen_width_x_sign <= SignHandler.__half_screen_width) == (
                                                                difference_in_screen_width_and_last_character_position <= SignHandler.__half_screen_width)
                        else:
                            self.signs[index].is_left = self.signs[index].pixel_coordinates_x[0] - \
                                                        self.signs[index].pixel_coordinates_x[-1] > 0

                            if False:#self.check_on_side(self.signs[index]):
                                print(config.INDEX_OF_All_FRAME)
                                self.signs[index].is_sign_side = True
                                self.azimuth = (self.azimuth + 90) % 360
                                self.side_signs.append(self.signs[index])
                            else:
                                # TODO удалить номер знака
                                if self.check_presence_of_nearby_sign(self.signs[index]):
                                    self.result_signs.append(self.signs[index])

                        signs_for_delete.append(self.signs[index])
        self.__signs_delete(signs_for_delete)

    def split_array(self,arr):
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]
        return left, right

    def __remove_incorrect_signs(self, current_frame_number):
        signs_for_delete = []
        for sign in self.signs:
            if sign.frame_numbers[-1] < (current_frame_number - SignHandler.__difference_frames_for_remove_sign):
                if sign.get_the_most_often(sign.result_CNN)['count'] < SignHandler.__min_length_sign:
                    signs_for_delete.append(sign)
        self.__signs_delete(signs_for_delete)

    def __add_new_unknown_element(self, frame, frame_sign_to_add):
        for item in frame:
            if item not in frame_sign_to_add:
                self.__add_sign(item)

    def __signs_delete(self, signs_for_delete):
        for sign in signs_for_delete:
            self.signs.remove(sign)

    def __check_pixel_coordinates(self, frame):
        vectors_matrix = []
        for sign in self.signs:
            vectors = []
            for item in frame:
                # Проверка на отрицательную высоту
                delta_h = item.y - sign.pixel_coordinates_y[-1]
                if delta_h <= 10:
                    delta_x = item.x - sign.pixel_coordinates_x[-1]
                    delta_y = item.y - sign.pixel_coordinates_y[-1]
                    # Теорема пифагора
                    vec = round((delta_x ** 2 + delta_y ** 2) ** 0.5, 0)
                    if sign.get_the_most_often(sign.result_yolo)['name'] == item.name_sign:
                        vec -= 50
                    else:
                        vec += 50
                    if vec > 800:
                        vec = SignHandler.__number_for_incorrect_evidences
                    vectors.append(vec)
                else:
                    vectors.append(SignHandler.__number_for_incorrect_evidences)
            vectors_matrix.append(vectors)
        index_min_sign = []
        for vectors in vectors_matrix:
            if vectors:
                index_min_sign.append([vectors.index(min(vectors)), min(vectors)])
        return index_min_sign


