import math
lat1 = 53.9448400000
lon1 = 27.4728166670
lat2 = 53.9448316670
lon2 = 27.4727083330
R = 6371  # Радиус Земли в километрах
d_lat = math.radians(lat2 - lat1)
d_lon = math.radians(lon2 - lon1)
a = (math.sin(d_lat / 2) ** 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * (
            math.sin(d_lon / 2) ** 2)
c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
distance = R * c
print(round(distance * 1000, 3))