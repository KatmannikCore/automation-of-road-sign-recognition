import pytesseract
from PIL import Image
import os
path = r'D:\Ur2\test10\118'
content = os.listdir(path)
import easyocr
# Создаем объект EasyOCR
reader = easyocr.Reader(['ru'])
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


#from google.cloud import vision
#from google.cloud.vision_v1 import types
#
## Инициализация клиента Google Cloud Vision
#client = vision.ImageAnnotatorClient()
#
## Загрузка изображения
#with open('image.png', 'rb') as image_file:
#    content = image_file.read()
#
#image = types.Image(content=content)
#
## Отправка изображения на распознавание текста
#response = client.text_detection(image=image)
#texts = response.text_annotations
#
#for text in texts:
#    print('\n"{}"'.format(text.description))