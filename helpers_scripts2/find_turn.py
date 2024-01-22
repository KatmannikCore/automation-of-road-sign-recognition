import math

def calculate_bearing(lat1, lon1, lat2, lon2):
    # Преобразуем все значения в радианы
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Вычисляем разницу между долготами
    d_lon = lon2 - lon1

    # Вычисляем угол bearing
    y = math.sin(d_lon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)
    bearing = math.atan2(y, x)

    # Преобразуем bearing из радиан в градусы
    bearing = math.degrees(bearing)

    # Нормализуем угол для получения значения от 0 до 360 градусов
    bearing = (bearing + 360) % 360

    if bearing > 180:
        return "влево"
    else:
        return "вправо"

# Пример использования функции
lat1, lon1 = 53.9429516670, 27.4801350000  # Начальные координаты
lat2, lon2 = 53.9429150000, 27.4796883330  # Конечные координаты

turn_direction = calculate_bearing(lat1, lon1, lat2, lon2)
print(f"Объект повернул {turn_direction} относительно своего движения.")

def determine_turn_direction(prev_lat, prev_long, current_lat, current_long):
    # Проверка на равенство координат
    if prev_lat == current_lat and prev_long == current_long:
        return "Объект не изменил своего положения"

    # Вычисление разницы между предыдущим и текущим положением
    delta_lat = current_lat - prev_lat
    delta_long = current_long - prev_long

    # Проверка направления изменения координат
    if delta_lat > 0 and delta_long > 0:
        return "Поворот вправо"
    elif delta_lat < 0 and delta_long < 0:
        return "Поворот влево"
    else:
        return "Нет явного поворота"

# Пример использования
prev_lat, prev_long = 53.9429516670, 27.4801350000
current_lat, current_long = 53.9429150000, 27.4796883330

result = determine_turn_direction(prev_lat, prev_long, current_lat, current_long)
print(result)