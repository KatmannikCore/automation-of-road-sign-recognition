import os
import glob
import shutil
directory = r"D:\Urban\yolov4\yolov4-opencv-python\test\blue\\"
for filename in os.listdir(directory):
    images = sorted(glob.glob(rf'{directory}{filename}\*.jpg'))

    for img in images:

        name = os.path.splitext(os.path.basename(img))[0]
        if len(name) < 15:
            if os.path.isfile(img):
                os.remove(img)
            #os.remove(rf'{directory}{filename}\{img}')
#path = r"D:\Urban\yolov4\darknet\build\darknet\x64\data\empty\\"
#images = sorted(glob.glob(rf'{path}*.jpg'))