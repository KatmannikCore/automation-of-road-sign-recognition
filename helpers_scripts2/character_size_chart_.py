import matplotlib.pyplot as plt

# Данные роста и веса
h1 = [44, 55, 56, 65, 61, 72]
w1 = [29, 33, 42, 38, 46, 46]
h2 = [23, 32, 30, 33, 35, 35, 45, 42, 42, 44, 48, 57, 62]
w2 = [25, 29, 30, 32, 33, 34, 38, 42, 39, 47, 43, 47, 49]
arr1 = [w1[index]/h1[index] for index in range(len(h1))]
arr2 = [w2[index]/h2[index] for index in range(len(h2))]
print(arr1)
print(arr2)

arr3 = [0.7, 0.6875, 0.7884615384615384, 0.59375, 0.7540983606557377, 0.9016393442622951]
# Создание графика
plt.figure(figsize=(10, 6))

# График зависимости h от w
plt.plot(arr1, label="Субъект 1")
plt.plot(arr2, label="Субъект 2")
#plt.plot(arr3, label="Субъект 3")

# Настройка графика
plt.xlabel("Вес")
plt.ylabel("Рост")
plt.title("Зависимость роста от веса")
plt.legend()

# Отображение графика
plt.show()

