import os
import glob
import shutil

from alive_progress import alive_bar

path = r"D:\Urban\yolov4\darknet\build\darknet\x64\data\empty\\"
images = sorted(glob.glob(rf'{path}*.jpg'))
with alive_bar(len(images), force_tty=True) as bar_dir:
    for img in images:
        bar_dir()
        name = os.path.splitext(os.path.basename(img))[0]+'.txt'
        open(path + name, "w+")
        #print(path + na me)