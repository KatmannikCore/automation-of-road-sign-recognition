from math import sqrt

def calculate_distance(x1, y1, x2, y2):
    distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

x1, y1 = 537217.5199812836, 537213.2523988726  # координаты первой точки
x2, y2 = 537210.6261943048, 537209.0942635225  # координаты второй точки

length = calculate_distance(x1, y1, x2, y2)
print(f"Длина отрезка между точками: {length} единиц")