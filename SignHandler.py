import math

import config
from Reader import Reader
from Sign import Sign
from itertools import groupby
class SignHandler:
    __number_for_incorrect_evidences = 9999.99
    __screen_width = 1920
    __half_screen_width = __screen_width/3
    __difference_frames_for_remove_sign = 10
    __difference_frames_for_move_sign = 5
    __frame_gap_between_sign = 5
    def __init__(self):
        self.Reader = Reader(config.PATH_TO_GPX )
        self.signs = []
        self.result_signs = []
        self.was_there_turn = False

    def check_the_data_to_add(self, frame):
        if frame:
            #Если знаков вообще нету
            if not self.signs:
                for sign in frame:
                    self.__add_sign(sign)
            else:
                if frame[0].number_frame == 63:
                    ...
                evidences = self.__check_pixel_coordinates(frame)
                evidences = self.__remove_collisions(evidences)
                frame_sign_to_add = self.__combine_frame_data_with_signs(evidences,frame)
                frame = self.__clean_frame(frame, frame_sign_to_add, evidences)
                self.__add_new_unknown_element(frame,frame_sign_to_add)
            current_number_frame = frame[0].number_frame
            self.__remove_incorrect_signs(current_number_frame)
            if not self.__is_turn():
                if self.was_there_turn:
                    self.was_there_turn = False
                    ...
                self.__move_final_signs(current_number_frame)

    def __is_turn(self):
        # TODO Сделать чтобы не учитывала точки ближе метра

        delta = self.Reader.get_azimuth(config.INDEX_OF_GPS + 1) - self.Reader.get_azimuth(config.INDEX_OF_GPS)


        is_turn = abs(delta) > 10
        if is_turn:
            print("В повороте")
            if delta < 0:
                print("Лево")
            else:
                print("Право")
            self.was_there_turn = True
            return True
        else:
            print("Прямо", end='\r')
            return False
    def __clean_frame(self, frame, frame_sign_to_add, evidences):
        not_added_signs = []
        for item in frame:
            if item not in frame_sign_to_add:
                not_added_signs.append(item)
        items_for_remove = []
        for index in range(len(evidences)):
            for item in not_added_signs:
                if self.signs[index].get_the_most_often(self.signs[index].result_yolo) == item.name_sign:
                    delta_x = item.x - self.signs[index].pixel_coordinates_x[-1]
                    delta_y = item.y - self.signs[index].pixel_coordinates_y[-1]
                    # Теорема пифагора
                    vec = round((delta_x ** 2 + delta_y ** 2) ** 0.5, 0)
                    if abs(vec - (evidences[index][1])) <= 30 and vec != 0:
                        self.signs[index].append_data(item)
                        items_for_remove.append(item)
        for item in items_for_remove:
            frame.remove(item)
        return  frame

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
  
    def __combine_frame_data_with_signs(self,evidences, frame):
        result = []
        for index in range(len(evidences)):
            if evidences[index][1] !=  SignHandler.__number_for_incorrect_evidences :
                if frame[0].number_frame - self.signs[index].frame_numbers[-1] < 7:
                    self.signs[index].append_data(frame[evidences[index][0]])
                    result.append(frame[evidences[index][0]])
        return result

    def __distance_on_earth(self,lat1, lon1, lat2, lon2):
        return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)

    def int_within_bounds(self, head, sub):
        head = int(round(head,0))
        sub = int(round(sub ,0))
        lower = sub - 10
        upper = sub + 10
        print(head, sub, lower, upper)
        return head in range(lower, upper)
    def check_presence_of_nearby_sign(self, sign):
        #sign.calculate_azimuth()
        for index in range(len(self.result_signs)):
            item = self.result_signs[index]

            average_item = sum(item.pixel_coordinates_x) / len(item.pixel_coordinates_x)
            average_sign = sum(sign.pixel_coordinates_x) / len(sign.pixel_coordinates_x)
            if average_sign != average_item:
                if item.is_left == sign.is_left:
                    if item.get_the_most_often(item.result_CNN) == sign.get_the_most_often(sign.result_CNN):
                        #item.calculate_azimuth()
                        #if not self.int_within_bounds(sign.get_azimuth(), item.get_azimuth()):
                        distance = self.__distance_on_earth(sign.car_coordinates_x[-1], sign.car_coordinates_y[-1], item.car_coordinates_x[-1], item.car_coordinates_y[-1])
                        if  distance < 20:
                            #print("Соеденены знаки:", self.result_signs[index], "и", sign)
                            self.result_signs[index].concat_2_object(sign)
                            return distance > 20
        return True
    def __move_final_signs(self,current_number_frame):

        signs_for_delete = []
        for index in range(len(self.signs)):
            different_frame = SignHandler.__difference_frames_for_move_sign + current_number_frame
            frame_for_sign = self.signs[index].frame_numbers[-1] + 20 #+ 10
            if( self.signs[index].is_sign_on_edge_of_screen() or len(self.signs[index].result_yolo) > 7) and frame_for_sign < different_frame: #or len(self.signs[index].result_yolo) > 7:
                #if frame_for_sign < different_frame:
                    if len(self.signs[index].result_yolo) >= SignHandler.__frame_gap_between_sign:
                        difference_in_screen_width_x_sign = SignHandler.__screen_width - self.signs[index].w[-1]
                        difference_in_screen_width_and_last_character_position = SignHandler.__screen_width - \
                                                                                 self.signs[index].pixel_coordinates_x[-1]
                        # Проверка 2х знаков на принадлежность к одной и тойже части экрана

                        if  len(self.signs[index].result_yolo) == 1:
                            self.signs[index].is_left = (difference_in_screen_width_x_sign <= SignHandler.__half_screen_width) == (
                                difference_in_screen_width_and_last_character_position <= SignHandler.__half_screen_width)
                        else:
                            self.signs[index].is_left = self.signs[index].pixel_coordinates_x[0] - self.signs[index].pixel_coordinates_x[-1] > 0
                        # TODO Проверка есть ли рядор знак
                        if self.check_presence_of_nearby_sign(self.signs[index]):
                            self.result_signs.append(self.signs[index])
                            #print("Добавлен знак:", self.signs[index])

                        #self.signs[index].car_coordinates_x = [el for el, _ in groupby(self.signs[index].car_coordinates_x)]
                        #self.signs[index].car_coordinates_y = [el for el, _ in groupby(self.signs[index].car_coordinates_y)]
                        signs_for_delete.append(self.signs[index])
        self.__signs_delete(signs_for_delete)
  
    def __remove_repeating_coordinates(self, sign):
        return [el for el, _ in groupby(sign)]
  
  
    def __remove_incorrect_signs(self,current_number_frame):
        signs_for_delete = []
        for sign in self.signs:
            if sign.frame_numbers[-1] < (current_number_frame - SignHandler.__difference_frames_for_remove_sign):
                if len(sign.result_yolo) <= SignHandler.__frame_gap_between_sign:
                    signs_for_delete.append(sign)
                    #print("Удаленный знак:",sign,'\n')
        self.__signs_delete(signs_for_delete)

 
    def __add_new_unknown_element(self, frame,frame_sign_to_add):
        for item in frame:
            if item not in frame_sign_to_add:
                self.__add_sign(item)
  
    def __signs_delete(self,signs_for_delete):
        for sign in signs_for_delete:
            self.signs.remove(sign)
  
    def __check_pixel_coordinates(self, frame):
        vectors_matrix = []
        for sign in self.signs:
            vectors = []
            for item in frame:

                #Проверка на отрицательную высоту
                delta_h = item.y - sign.pixel_coordinates_y[-1]
                if delta_h <= 5:

                    delta_x = item.x - sign.pixel_coordinates_x[-1]
                    delta_y = item.y - sign.pixel_coordinates_y[-1]
                    #Теорема пифагора
                    vec = round((delta_x**2 +  delta_y**2) ** 0.5, 0)
                    if vec > 800:
                        vec = SignHandler.__number_for_incorrect_evidences
                    if sign.get_the_most_often(sign.result_yolo) == item.name_sign:
                        vec -= 50
                    vectors.append(vec)
                else:
                    vectors.append(SignHandler.__number_for_incorrect_evidences)
            vectors_matrix.append(vectors)
        index_min_sign = []
        for vectors in vectors_matrix:
            if vectors:
                index_min_sign.append([vectors.index(min(vectors)), min(vectors)])
        return index_min_sign
 
    def __check_frames(self,frame):
        frame_number_coefficient = 10
        number_frame = frame[0].number_sign
        results = []
        for sign in self.signs:
            result = number_frame - frame_number_coefficient < sign.frame_numbers[-1]
            results.append(result)
        return results
    def __check_type(self, frame):
        matrix = []
        for sign in self.signs:
            arr = []
            for index in range(len(frame)):
                if sign.get_the_most_often(sign.result_yolo) == frame[index].name_sign:
                    arr.append(index)
            matrix.append(arr)
        return matrix
