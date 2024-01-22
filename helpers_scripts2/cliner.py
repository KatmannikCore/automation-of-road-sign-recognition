import os

import pandas as pd
from alive_progress import alive_bar
import random
import config
from PIL import Image
import shutil
path = r"D:\Urban\test\try\\"
path_tresh = r"D:\Urban\test\try_trash"
content = os.listdir(path)
myvar = pd.DataFrame(config.DEVIATION_RANGE, index=["range_min_h", "range_max_h", "range_min_w", "range_max_w",])
print(myvar)
myvar.to_csv('myvar.csv')
files = []
with alive_bar(len(content), force_tty=True) as bar_dir:
    for folder in content:
        bar_dir()
        new_path = rf"{path}{folder}"
        files = os.listdir(new_path)
        path_trash_folder = rf"{path_tresh}\{folder}_trash"
        if not os.path.exists(path_trash_folder): os.makedirs(path_trash_folder)
        #print(config.DEVIARTION[int(folder)])
        deviation = config.DEVIATION_RANGE[int(folder)]
        for file in files:
            path_img = rf"{new_path}\{file}"
            path_trash_img = rf"{path_trash_folder}\{file}"
            try:
                with Image.open(path_img) as img:
                    width, height = img.size
                    h = round(height/width,2)
                    w = round(width/height,2)
                    if deviation["range_min_h"] <= h <= deviation["range_max_h"] and deviation["range_min_w"] <= w <= deviation["range_max_w"]:
                        pass
                        #print(deviation["range_min_h"] <= h <= deviation["range_max_h"],
                        #      deviation["range_min_w"] <= w <= deviation["range_max_w"])
                    else:
                        x = deviation["range_min_h"]
                        y = deviation["range_max_h"]
                        z = deviation["range_min_w"]
                        a = deviation["range_max_w"]
                        ae = random.randint(0, 9999999)
                        img.close()
                        shutil.copy2(path_img, rf"{path_trash_folder}\{x}_{h}_{y}______{z}_{w}_{a}___{ae}.jpg")
                        os.remove(path_img)
                        #files.append(path_img)
            except Exception as e:
                pass
#for item in files:
#