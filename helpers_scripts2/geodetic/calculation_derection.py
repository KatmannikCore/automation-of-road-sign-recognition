def calculate_azimuth_change(old_azimuth, new_azimuth):
    azimuth_change = new_azimuth - old_azimuth
    if azimuth_change > 180:
        azimuth_change = azimuth_change - 360
    elif azimuth_change < -180:
        azimuth_change = azimuth_change + 360
    return azimuth_change

# Пример использования:
old_azimuth = 30
new_azimuth = 320
azimuth_change = calculate_azimuth_change(old_azimuth, new_azimuth)
print(f'Изменение азимута: {azimuth_change} градусов')