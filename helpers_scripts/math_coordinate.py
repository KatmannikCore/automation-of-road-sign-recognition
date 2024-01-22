import math
from Converter import Converter
converter = Converter()
# Координаты известных вершин
x1, y1 = 536256.5262947647, 5974668.776853883
x2, y2 = 536265.5167054327, 5974652.898937749
dx =  x2 - x1
dy =  y2 - y1
# Длины сторон треугольника (это просто для примера, я использую произвольные значения)
#side_a = (dx**2 +dy**2)**0.5  # замените на фактическое значение
#side_b = side_a  # замените на фактическое значение
#side_c =  (side_a**2 +side_b**2)**0.5  # замените на фактическое значение
#
## Найдем расстояние между известными вершинами
#d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
#
## Используем закон косинусов, чтобы найти угол между сторонами a и d
#cos_angle_A = (side_b**2 + d**2 - side_c**2) / (2 * side_b * d)
#
## Найдем угол A в радианах
#angle_A = math.acos(cos_angle_A)
#
## Используем найденный угол и расстояние от первой вершины, чтобы найти координаты третьей вершины
#x3 = x1 + side_a * math.cos(angle_A)
#y3 = y1 + side_a * math.sin(angle_A)
x3 = x1 - dy
y3 = y1 + dx
#
x1, y1  = converter.coordinateConverter(x1, y1 , "epsg:32635", "epsg:4326")
x2, y2  = converter.coordinateConverter(x2, y2 , "epsg:32635", "epsg:4326")
x3, y3 = converter.coordinateConverter(x3, y3, "epsg:32635", "epsg:4326")
print(f"Координаты первой вершины: ({x1}, {y1})")
print(f"Координаты второй вершины: ({x2}, {y2})")
print(f"Координаты третьей вершины: ({x3}, {y3})")
