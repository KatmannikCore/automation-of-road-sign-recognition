import os
for root, dirs, files in os.walk(r"D:\Urban\yolov4\yolov4-opencv-python\kal"):
    for filename in files:
        name_jpg =  os.path.splitext(os.path.basename(filename))[0] + '.jpg'
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), r'E:\recognition_sings\NaselennuePunkty\img'+'\\'+name_jpg)
        os.remove(path)