#from geopy.distance import geodesic
#from geopy.point import Point
#
## Прямая геодезическая задача
#point_a = Point(53.9448400000, 27.4728166670)  # Координаты Нью-Йорка
#point_b = Point(53.9448050000, 27.4726700000)  # Координаты Лос-Анджелеса
#
## Расстояние между двумя точками
#distance = geodesic(point_a, point_b).kilometers
#
## Направление от точки A к точке B
#azimuth = geodesic(point_a, point_b).destination(point_a, 0)
#
#print("Прямая геодезическая задача:")
#print("Расстояние между точками A и B:", distance, "км")
#print("Направление от точки A к точке B:", azimuth, "градусов")
#
## Обратная геодезическая задача
## Зададим начальную точку A
#point_a = Point(40.7128, -74.0060)  # Координаты Нью-Йорка
#
## Направление и расстояние
#azimuth = 45  # Направление на северо-восток
#distance = 100  # Расстояние в км
#
## Решение обратной геодезической задачи
#point_b = geodesic().destination(point=point_a, bearing=azimuth, distance=distance)
#
#print("\nОбратная геодезическая задача:")
#print("Координаты точки B:", point_b.latitude, point_b.longitude)


from pygeoguz.simplegeo import *
from pygeoguz.objects import *
from Converter import Converter
Converter = Converter()
#53.9448400000, 27.4728166670
#53.9448050000, 27.4726700000

#531033.7667604118 5977488.084138459
#531024.1661724359 5977484.125883081

y1, x1 = 531034.198098322 , 5977489.01458451
y2, x2 = 531032.5089653846, 5977496.235426282

p2 = Point2D( x1, y1)
p1 = Point2D( x2, y2)
line = ogz(point_a=p1, point_b=p2)

length = line.length
direction = line.direction
print(length, direction )

from pygeoguz.simplegeo import *
from pygeoguz.objects import *

#p1 = Point2D(531033.7667604118, 5977488.084138459)
line = Line2D(length=length, direction=direction + 30 +6)
p2 = pgz(point=p1, line=line)

x = p2.x
y = p2.y
x1, y1 = Converter.coordinateConverter(y, x, "epsg:32635", "epsg:4326")
print(x1)
print(y1)