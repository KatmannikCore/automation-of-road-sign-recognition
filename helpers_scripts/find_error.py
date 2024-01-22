import os
import glob
import shutil

from skimage.io import imread, imsave
path_to_trash = r"D:\Ur2\next\29"
path_to_save = r"D:\Ur2\valid\\"
path_to_img = r"D:\Urban\yolov4\darknet\build\darknet\x64\data\obj\\"
images = sorted(glob.glob(r'D:\Ur2\next\29\*.jpg'))
for img in images:
   # try:
        name = os.path.splitext(os.path.basename(img))[0]+'.jpg'
        print(name)
        where = path_to_save + name
        from_where =path_to_img + name
        shutil.copy2(from_where, where)
   # except Exception as e:
    #    print("error", e)