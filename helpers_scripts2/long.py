from math import sqrt

def calculate_distance(x1, y1, x2, y2):
    distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

x1, y1 = 537217.5199812836, 537213.2523988726  # координаты первой точки
x2, y2 = 537210.6261943048, 537209.0942635225  # координаты второй точки

length = calculate_distance(x1, y1, x2, y2)
print(f"Длина отрезка между точками: {length} единиц")


from geopy.distance import geodesic

# Заданные географические координаты
coordinates = [(53.944301667, 27.461348333), (53.94432, 27.461246667), (53.944315, 27.461125), (53.944283333, 27.461)]

# Вычисление длины кривой по заданным координатам
total_distance = 0
for i in range(len(coordinates) - 1):
    total_distance += geodesic(coordinates[i], coordinates[i + 1]).meters

print("Длина кривой составляет: {:.2f} метров".format(total_distance))


