import os
import shutil

from Detector import Detector
import cv2

dir_for_learning = [r"D:\Urban\yolov4\OpenLabeling-master\main\input"]
#r"D:\Urban\learning\auto\GP100056 (22.09.2022 9-42-23)",
#r"D:\Urban\learning\auto\GP100057 (16.09.2022 9-11-49)",
#r"D:\Urban\learning\auto\GP100059 (21.09.2022 12-45-51)",
#r"D:\Urban\learning\auto\GP100077 (22.09.2022 14-49-04)",
#r"D:\Urban\learning\auto\GP100079 (23.09.2022 10-48-50)",
#r"D:\Urban\learning\auto\GP100082 (23.09.2022 15-16-30)",
#r"D:\Urban\learning\auto\GP100083 (26.09.2022 9-57-47)",GP070079 (23.09.2022 10-31-06)
#r"D:\Urban\learning\auto\GP110056 (22.09.2022 9-34-31)"]
detector = Detector()

classes = {

"parkovka":0,
"treugolnik":1,
"krug":2,
"glavnaya doroga":3,
"peshehodnyj perehod":4,
"ostanovka i parkovka zapreshena":5,
"viezd na dorogu s odnostorinnim dvizeniem >":6,
"napravlenie dvizheniya po polosam":7,
"ustupi dorogu":8,
"red":9,
"zhilaya zona":10,
"tupik":11,
"polosa dlya obshestvennogo transporta":12,
"blue":13,
"servises":14,
"konec odnostoronnego dvizheniya":15,
"tablichka |":16,
"tablichka __":17,
"ostanovka avtobusa tablichka":18,
"doroga s odnostoronnim dvizheniem":19,
"napravlenie glavnoj dorogi":20
}

width = 1920
height = 1080
for dir in dir_for_learning:
    imgList = os.listdir(dir)
    for img_path in imgList:
        if img_path[14:] == '.jpg':

            image = cv2.imread(rf"{dir}\{img_path}")
            rectangles = detector.find_rectangles(image)
            if len(rectangles) == -1:
                shutil.move(os.path.join(dir, img_path), os.path.join(rf'{dir}\empty', img_path))
                print(len(rectangles))
                print(rf"{dir}\{img_path}")
            else:
                my_file_name = fr"{dir}\{img_path[:14]}.txt"
                my_file = open(my_file_name, "w+")
                result_data = []
                for box, color, label, name_sing in rectangles:
                    point_1 = [box[0], box[1]]
                    point_2 = [box[0] + box[2],  box[1] + box[3]]
                    x_center = float((point_1[0] + point_2[0]) / (2.0 * width))
                    y_center = float((point_1[1] + point_2[1]) / (2.0 * height))
                    x_width = float(abs(point_2[0] - point_1[0])) / width
                    y_height = float(abs(point_2[1] - point_1[1])) / height
                    items = map(str, [classes[name_sing], x_center, y_center, x_width, y_height])
                    result_data.append(' '.join(items))
                if len(result_data) != 0:
                    my_file.write('\n'.join(result_data) + '\n')
                my_file.close()
                print(my_file_name)
        #cv2.imshow("Image", image)
        cv2.waitKey(1)