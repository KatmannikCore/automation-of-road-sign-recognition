import math
def azimuth_difference(azimuth1, azimuth2):
  """Вычисляет разницу между двумя азимутами.

  Args:
    azimuth1: Первый азимут в градусах.
    azimuth2: Второй азимут в градусах.

  Returns:
    Разница между двумя азимутами в градусах.
  """

  # Преобразуем азимуты в радианы.
  azimuth1_rad = azimuth1 * math.pi / 180
  azimuth2_rad = azimuth2 * math.pi / 180

  # Вычисляем разницу между азимутами.
  difference = azimuth2_rad - azimuth1_rad

  # Обернём значение разницы в диапазон от 0 до 2π.
  difference = (difference + 2 * math.pi) % (2 * math.pi)

  # Преобразуем разницу в градусы.
  difference_deg = difference * 180 / math.pi

  return difference_deg


# Пример использования
azimuth1 = 11
azimuth2 = 352
difference = azimuth_difference(azimuth1, azimuth2)
print(f"Разница между азимутами {azimuth1} и {azimuth2}: {difference} градусов")