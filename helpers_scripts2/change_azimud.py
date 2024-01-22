import math

# Изначальный азимут в градусах
initial_azimuth_degrees = 350

# Угол поворота также в градусах
rotation_angle_degrees = 90

# Конвертируем азимуты в радианы
initial_azimuth_radians = math.radians(initial_azimuth_degrees)
rotation_angle_radians = math.radians(rotation_angle_degrees)
# Суммарный азимут после поворота
result_azimuth_radians = (initial_azimuth_radians + rotation_angle_radians) % (2 * math.pi)

# Конвертируем суммарный азимут обратно в градусы
result_azimuth_degrees = math.degrees(result_azimuth_radians)
#print(result_azimuth_degrees)

initial_azimuth = 150
final_azimuth = 175

# Находим изменение азимута
azimuth_change = (final_azimuth - initial_azimuth) % 360

print(azimuth_change)

