import glob
import os
import shutil
import pandas as pd
import copy
from static import convert_YOLO_to_normal
from static import classifier
from PIL import Image
from alive_progress import alive_bar
import numpy as np
import matplotlib.pyplot as plt
from scipy. stats import norm
import seaborn as sns

def get_statistics_from_dataset():
    path = r"D:\Urban\yolov4\darknet\build\darknet\x64\data\obj"
    files = sorted(glob.glob(rf'{path}\*.txt'))
    arr_area = {}
    for item in range(len(classifier)):
        arr_area[item] = []
    print(arr_area)
    with alive_bar(len(files), force_tty=True) as bar_dir:
        for File in files:
            bar_dir()

            with open(os.path.join(path, File), 'r') as file:
                lines = file.readlines()
            for line in lines:
                try:
                    new_line = line.split(" ")
                    h, w = convert_YOLO_to_normal(new_line)
                    area = h*w
                    #if area < 10000:
                    arr_area[int(new_line[0])].append(area)
                except Exception as e:
                    print("error", e)
    plt.subplot(1, 2, 1)
    sns.countplot( data=arr_area[0])
    plt.subplot(1, 2, 2)
    sns.displot(arr_area[0],  height=5)
    plt.show()
get_statistics_from_dataset()



def get_statistics_from_test_data():
    path = r"D:\Urban\test\try\0"
    files = sorted(glob.glob(rf'{path}\*.jpg'))
    result_arr = []
    with alive_bar(len(files), force_tty=True) as bar_dir:
        for File in files:
            bar_dir()
            with Image.open(File) as img:
                width, height = img.size
                area =  width * height
                #if area < 10000:
                result_arr.append(area)
    sns.displot(result_arr)
    plt.show()
#get_statistics_from_test_data()