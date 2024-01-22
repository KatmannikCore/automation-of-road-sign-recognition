import os

import cv2
from alive_progress import alive_bar
from matplotlib import pyplot as plt
from PIL import Image
path = r"D:\Urban\yolov4\darknet\build\darknet\x64\data\obj"
dir = os.listdir(path)
save_img = r"D:\Urban\yolov4\yolov4-opencv-python\big_test\\"
cont = 0
for num in range(0,30):
    os.makedirs(save_img +"\\"+ str(num))
#with alive_bar(len(dir), force_tty=True) as bar_dir:
#    for filename in dir:
#        bar_dir()
#        if filename.endswith('.txt'):
#            with open(os.path.join(path, filename), 'r') as file:
#                lines = file.readlines()
#                for line in lines:
#                    try:
#                        new_line = line.split(" ")
#                        pathDir_for_img = save_img + new_line[0]
#                        if not os.path.exists(pathDir_for_img): os.makedirs(pathDir_for_img)
#                        x_center = float(new_line[1]) * 1920.0
#                        y_center = float(new_line[2]) * 1080.0
#                        x_width = (float(new_line[3]) * 1920.0)  / 2.0
#                        y_height =(float(new_line[4]) * 1080.0) / 2.0
#                        xmin = int(round(x_center - x_width))
#                        ymin = int(round(y_center - y_height))
#                        xmax = int(round(x_center + x_width))
#                        ymax = int(round(y_center + y_height))
#                        path_to_img = fr"{path}\{filename.split('.')[0]}.jpg"
#                        img =  Image.open(path_to_img)
#                        im_crop = img.crop((xmin, ymin, xmax, ymax))
#                        save_to_img = f"{pathDir_for_img}/{filename.split('.')[0]}.jpg"
#                        im_crop.save(save_to_img, quality=100)
#                    except Exception as e:
#                        print("error", e)
#
#
