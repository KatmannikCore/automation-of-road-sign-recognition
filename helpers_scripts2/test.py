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