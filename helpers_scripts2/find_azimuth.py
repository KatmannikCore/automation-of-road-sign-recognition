from geopy.distance import geodesic
from math import atan2, degrees, radians
import math

def calculate_bearing(coord1, coord2):
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    d_lon = lon2 - lon1

    y = math.sin(d_lon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)
    bearing = atan2(y, x)

    return (degrees(bearing) + 360) % 360


coord1 = (53.9189633409,  27.5660590737)  # пример координат точки 1 (широта, долгота)
coord2 = (53.9188948936, 27.5661996345)  # пример координат точки 2 (широта, долгота)

azimuth = calculate_bearing(coord1, coord2)
print(f"Азимут от точки 1 до точки 2: {azimuth} градусов")

# Изначальный азимут и конечный азимут
initial_azimuth = 20
final_azimuth = 50

# Находим изменение азимута
azimuth_change = (final_azimuth - initial_azimuth) % 360

print(  initial_azimuth- final_azimuth, azimuth_change)


