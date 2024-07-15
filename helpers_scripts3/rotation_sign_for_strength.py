import json
import matplotlib.pyplot as plt
import pylab
from termcolor import colored
file_path = 'sample.json'
from termcolor import colored
import pandas as pd
def split_array( arr):
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    return left, right


with open(file_path, 'r') as file:
    # Загружаем данные из JSON файла
    data = json.load(file)['objects']
    for item in data:

        name_one = item['name_one']
        name_two = item['name_two']

        w = item['w']
        h = item['h']
        x = item['x']
        y = item['y']

        length = item['length']
        if length < 4:
            continue
        number = item['number'] - 63600
        if number > 63600:
            number = number - 63600
        frame = round(number / 60, 0)
        minute = int(frame / 60)
        part_seconds = (frame / 60 ) - minute
        seconds = int(60 * part_seconds)
        max_w = max(w)
        max_h = max(h)
        min_w = min(w)
        min_h = min(h)
        names_signs_for_side = ["parkovka", "ostanovka i parkovka zapreshena", "krug", "red", "tupik", "zhilaya zona",
                                "red"]
        CS = (max_w * max_h) / (min_h * min_w)
        proportions = [w[index] / h[index] for index in range(len(h))]
        left_half, right_half = split_array(proportions)

        if not left_half:
            continue

        different_left = abs(min(left_half) - max(left_half))
        different_right = abs(min(right_half) - max(right_half))
        average = sum(proportions) / len(proportions)
        bol = False
        print((max(x)-min(x))/len(w))
        bol =  (CS < 10 and \
               (max_w * max_h) < 20500 and \
               x[0] > 1000 and \
               len(w) >= 4 and \
               name_one in names_signs_for_side and \
               (round(different_left, 1) > round(different_right, 1) or average < 0.75)) #or (CS < 2)
        #if bol:
        #    print('\033[0;0m')
        #else:
        #    print( "\033[1;31m")
        if bol:
            #print(left_half, "\n",right_half)
            print(f"Time: {minute}.{seconds}")

            print(item)
            #print(f'CS:{CS}\n'
            #      f' x:{x[0]}\n '
            #      f'len:{len(w)} \n '
            #      f'{round(different_left, 1)} > {round(different_right, 1)} {round(different_left, 2) > round(different_right, 2) or average < 0.7}\n '
            #      f'average:{average}\n'
            #      f'{average < 0.75 and abs(different_right - different_left + abs(average - 0.75)) > 1.5} dr: {different_right} dl: {different_left} dr-dl: {different_right - different_left} res: {abs(different_right - different_left + abs(average - 0.75))}\n'
            #      f'bol: {bol}\n')
            arr = [w[index] / h[index] for index in range(len(h))]
            new_arr = []
            for index in range(len(item["h"])):
                new_arr.append(item["h"][index]/item["w"][index])
            #print(new_arr)
            #plt.figure(figsize=(12, 7))
            #plt.subplot(2, 2, 1)
            #plt.plot(new_arr)
            #plt.subplot(2,2, 2)
            #plt.plot( item["w"])
            #plt.subplot(2,2, 3)
            #plt.plot(new_arr)
            #plt.subplot(2, 2, 4)
            #plt.plot([1,2])
            #plt.text(0.7,0.7, f'CS:{CS}\n x:{x[0]}\n len:{len(w)} \n {different_left > different_right or average < 0.9}\n bol: {bol}', backgroundcolor='yellow')
            #plt.show()