import os
import shutil

from Detector import Detector
import cv2

dir_for_learning = [r"E:\signs\GOPR0451 (18.06.2024 9-58-35)",
                    r"E:\signs\GOPR0550 (18.06.2024 10-01-35)",
                    r"E:\signs\GP010451 (18.06.2024 9-59-21)",
                    r"E:\signs\GP010461 (18.06.2024 10-00-37)",
                    r"E:\signs\GP010550 (18.06.2024 10-02-25)",
                    r"E:\signs\GP020461 (18.06.2024 10-01-23)",
                    r"E:\signs\GP020550 (18.06.2024 10-03-19)",
                    r"E:\signs\GP030550 (18.06.2024 10-04-12)",
                    r"E:\signs\GP040550 (18.06.2024 10-05-09)",
                    r"E:\signs\GP050550 (18.06.2024 10-06-07)",
                    r"E:\signs\GP060550 (18.06.2024 10-06-55)",
                    r"E:\signs\GP070550 (18.06.2024 10-07-43)",
                    r"E:\signs\GP080550 (18.06.2024 10-08-33)",
                    r"E:\signs\GP090550 (18.06.2024 10-09-21)",
                    r"E:\signs\GP100550 (18.06.2024 10-10-09)",]
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
"napravlenie glavnoj dorogi":20,
"nachalo nas punkta bel s dom": 21,
"konec nas punkta bel s dom": 22,
"nachalo nas punkta bel": 23,
"konec nas punkta bel": 24,
"nachalo nas punkta sin": 25,
"konec nas punkta sin": 26,
"Sbros vseh ogranicheniu": 27,
"platnaua doroga": 28
}

width = 1920
height = 1080
for dir in dir_for_learning:
    imgList = os.listdir(dir)
    for img_path in imgList:
        if img_path.split('.')[-1] == 'jpg':

            image = cv2.imread(rf"{dir}\{img_path}")
            rectangles = detector.find_rectangles(image)
            if len(rectangles) == -1:
                shutil.move(os.path.join(dir, img_path), os.path.join(rf'{dir}\empty', img_path))
                print(len(rectangles))
                print(rf"{dir}\{img_path}")
            else:
                my_file_name = fr"{dir}\{img_path.split('.')[0]}.txt"
                my_file = open(my_file_name, "w+")
                result_data = []
                for box, color, label, name_sing, res, text_on_sign in rectangles:
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