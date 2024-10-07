import glob
import os
from json import dump

import cv2
import geojson
from geojson import FeatureCollection, Feature

file_path = "./video.mp4"
cap = cv2.VideoCapture(rf"D:\Urban\vid\test\GOPR0064\GP010064.MP4")
frame_number = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
from configs import config

result = []
with open(config.PATH_TO_GEOJSON) as f:
    data = geojson.load(f)
counter = 0

for feature in data['features']:
    for item in feature["properties"]:
        features = []
        frame_number = None
        frame_number = float(feature["properties"]['absolute_frame_numbers'][-3])
        result.append(feature)
        #if item == 'MVALUE' and feature["properties"]['MVALUE'] == "":
        #    frame_number = float(feature["properties"]['absolute_frame_numbers'][-3])
        #    result.append(feature)
        #if feature["properties"]['type'] == "5.8.1":
        #    frame_number = float(feature["properties"]['absolute_frame_numbers'][-3])
        #    result.append(feature)
        #if feature["properties"]['type'] == "3.1" or feature["properties"]['type'] == "3.2":
        #    frame_number = float(feature["properties"]['absolute_frame_numbers'][-3])
        #    result.append(feature)
        if frame_number != None:
            print(frame_number)
            features.append(Feature(geometry=feature["geometry"], properties=feature["properties"]))
            feature_collection = FeatureCollection(features)

            number_video = int(frame_number // 63600)
            frame_number_for_save = int(frame_number % 63600)
            files = os.listdir(config.PATH_TO_VIDEO)
            new_path = os.path.join(config.PATH_TO_VIDEO, str(files[number_video]))
            cap = cv2.VideoCapture(new_path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number_for_save)
            ret, frame = cap.read()
            while not ret:
                ret, frame = cap.read()
            frame = cv2.resize(frame, dsize=(960, 540))
            cv2.imwrite(rf'./errorData/{str(counter)}.jpg', frame)
            with open(rf'./errorData/{str(counter)}.geojson', 'w') as f:
                geojson.dump(feature_collection, f)
            #cv2.waitKey(1000)
            counter += 1
            break