#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pytesseract
from PIL import Image
import os

from textblob.en import Spelling
from rapidfuzz import fuzz
from textblob import TextBlob






path = r'D:\Ur2\test10\118'
content = os.listdir(path)
import easyocr
# Создаем объект EasyOCR
reader = easyocr.Reader(['be'])
for im in content:

        path_img = path + '\\' + im
        result = reader.readtext(path_img)
        if result:
            for (bbox, text, prob) in result:
                #print(im,': ',text, prob)
                print(text)
        else:
            ...
           # print(im, ': empty')


