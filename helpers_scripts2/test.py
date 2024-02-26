
from geopy.point import Point
from pyproj import Geod

from Converter import Converter
Converter = Converter()
# Исходные координаты
lat1 = 53.9448483367
lon1 = 27.4728233330
lat2 = 53.9449133367
lon2 = 27.4727983330
x1, y1 = Converter.coordinateConverter(lat1, lon1, "epsg:4326", "epsg:32635")
x2, y2 = Converter.coordinateConverter(lat2, lon2, "epsg:4326", "epsg:32635")
#3.89
#   531024.1661724359 5977484.125883081
#   531026.6623898167 5977487.10958937
print(x1, y1)
print(x2, y2)

lat3 = 531025.6663177015
lon3 = 5977491.522572389


x3, y3 = Converter.coordinateConverter(lat3, lon3, "epsg:32635", "epsg:4326")
print(x3, y3)
azimuth = 28  # Азимут в градусах
distance = 5  # Расстояние в метрах

# Создаем объект Geod для вычисления геодезических расстояний
geod = Geod(ellps='WGS84')

# Вычисляем новую точку
#new_lat, new_lon, _ = geod.fwd(lon, lat, azimuth, distance)

#print("Новые координаты:")
#print("Широта:", new_lat)
#print("Долгота:", new_lon)

from PIL import Image
import pytesseract

# Укажите путь к исполняемому файлу tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Urbanovich\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Укажите путь к изображению, с которого нужно считать текст
image_path = r'D:\Urban\yolov4\yolov4-opencv-python\train\54\0_1.0%.jpg'

# Открываем изображение
img = Image.open(image_path)

# Используем pytesseract для извлечения текста с изображения
text = pytesseract.image_to_string(img, lang='rus')

print(text)

import easyocr

# Инициализация ридера
reader = easyocr.Reader(['ru'])  # Укажите язык или языки, которые вы хотите распознавать

# Чтение текста с изображения
result = reader.readtext(image_path)

# Вывод результатов
for (bbox, text, prob) in result:
    print(f'Текст: {text} (Вероятность: {prob:.2f})')

