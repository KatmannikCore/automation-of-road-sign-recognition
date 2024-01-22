import glob
import os
import shutil
import pandas as pd
import copy
from PIL import Image
import statistics
from alive_progress import alive_bar

arr_avr = {}
from static import convert_YOLO_to_normal
from static import classifier

for item in range(len(classifier)):
    arr_avr[item] = [[],[]]
path = r"D:\Urban\yolov4\darknet\build\darknet\x64\data\obj"
files = sorted(glob.glob(rf'{path}\*.txt'))
with alive_bar(len(files), force_tty=True) as bar_dir:
    for file in files:
        bar_dir()
        with Image.open(file.split('.')[0]+".jpg") as img:
            width, height = img.size
        if width/height >= 5:
            print(width, height, width/height, file.split('.')[0]+".jpg")
        if height/width >= 5:
            print(height, width,height/width, file.split('.')[0]+".jpg")
        with open(os.path.join(path, file), 'r') as file:
            lines = file.readlines()
        for line in lines:
            try:
                new_line = line.split(" ")
                h, w = convert_YOLO_to_normal(new_line)

                if w / h >= 5:
                    print(w, h, w / h)
                    print(file)
                    #print(file.split('.')[0] + ".jpg")
                if h / w >= 5:
                    print(h, w, h / w)
                    print(file)
                arr_avr[int(new_line[0])][0].append(h)
                arr_avr[int(new_line[0])][1].append(w)
                #print(arr_avr[0])
                #print((xmin, ymin, xmax, ymax))
            except Exception as e:
                print("error", e)

result_arr = {}
for item in range(len(classifier)):
    result_arr[item] = [[],[]]


arr_avr[17][0][10725] = 8
arr_avr[28][1][30] = 50
with alive_bar(len(result_arr), force_tty=True) as bar_dir:
    for item in result_arr:
        prop_h = []
        prop_w = []
        bar_dir()
        #print(arr_avr[item][0], arr_avr[item][1])
        result_arr[item][0] = round(sum(arr_avr[item][0]) / len(arr_avr[item][0]), 2)
        result_arr[item][1] = round(sum(arr_avr[item][1]) / len(arr_avr[item][1]), 2)

        for index in range(len(arr_avr[item][0])):
            #print(index, item)
            prop_h.append(round(arr_avr[item][0][index] / arr_avr[item][1][index], 1))
            prop_w.append(round(arr_avr[item][1][index] / arr_avr[item][0][index], 1))
        #prop_h.append(round(arr_avr[item][0] / arr_avr[item][1], 2))
        #prop_w.append(round(arr_avr[item][1] / arr_avr[item][0], 2))
        result_arr[item].append(max(arr_avr[item][0]))
        result_arr[item].append(min(arr_avr[item][0]))
        result_arr[item].append(max(arr_avr[item][1]))
        result_arr[item].append(min(arr_avr[item][1]))
        result_arr[item].append(round(result_arr[item][0] * result_arr[item][1], 2))
        result_arr[item].append(round(result_arr[item][0] / result_arr[item][1], 2))
        result_arr[item].append(round(result_arr[item][1] / result_arr[item][0], 2))
        result_arr[item].append(round(statistics.stdev(prop_h, xbar=None), 1))
        result_arr[item].append(round(statistics.stdev(prop_w, xbar=None), 1))
        result_arr[item].append(max(prop_h))
        result_arr[item].append(max(prop_w))



dates = ["H","W","max_h", "min_h","max_w", "min_w", "s", "h/w", "w/h", "Stat h/w", "Stat w/h", "max h", "max w"]
myvar = pd.DataFrame(result_arr, index=dates)
print(myvar)
myvar.to_csv('myvar.csv')