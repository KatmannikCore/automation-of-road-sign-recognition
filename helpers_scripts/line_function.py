
import numpy as np

# скорость автомобиля, km/h
speed = np.array([17, 15, 12, 8, 5, 3])
# время обработки данных, секунды
processing_time = np.array([2, 3, 4, 6, 8, 10])
#[5, 6, 7, 8, 9, 10] k = -0.3 b = 10.83
#[2, 3, 4, 6, 8, 10] k = -0.5 b = 10.9
# аппроксимация данных методом наименьших квадратов,
# длина массива коэффициентов равна степени полинома
# в данном случае 1 полином
coefficients = np.polyfit(speed, processing_time, 1)

# уравнение прямой y = kx + b
k, b = coefficients

print(f"k = {k} sec/(km/h), b = {b} sec")

# скорость автомобиля 35 km/h, время обработки данных
processing_time = k * 4 + b

print(f"Время обработки данных для машины со скоростью 35 km/h составляет {processing_time:.1f} секунды")



# скорость автомобиля, m/s
speed = np.array([17, 15, 12, 8, 5, 3])
# время обработки данных, секунды
processing_time = np.array([5, 6, 7, 8, 9, 10])

sum = 0
for index in range(6):
    print(speed[index])
    sum += speed[index] + processing_time[index]

print(sum)
# аппроксимация данных методом наименьших квадратов,
# длина массива коэффициентов равна степени полинома
# в данном случае 1 полином
coefficients = np.polyfit(speed, processing_time, 1)

# уравнение прямой y = kx + b
k, b = coefficients

print(f"k = {k} sec/m, b = {b} sec")

# скорость автомобиля 35 km/h, время обработки данных
processing_time = k * (1.543333) + b # переводим скорость в метры в секунду

print(f"Время обработки данных для машины со скоростью 35 km/h составляет {processing_time:.1f} секунды")
