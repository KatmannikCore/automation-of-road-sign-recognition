import matplotlib.pyplot as plt
w = [24, 24, 24, 24, 26, 25, 25, 26, 27, 28, 29, 24, 34, 34, 35, 39, 43, 47, 47, 53, 50, 60, 60, 54, 62, 46, 32, 22, 26, 28, 27, 27, 29, 28, 27, 27, 34, 37, 39, 44, 44, 47, 52, 55, 57, 62]
h = [40, 40, 44, 41, 44, 48, 42, 45, 43, 45, 48, 57, 55, 66, 69, 62, 64, 62, 65, 64, 80, 76, 75, 87, 74, 78, 86, 86, 42, 48, 46, 46, 47, 48, 54, 56, 60, 62, 55, 57, 61, 62, 62, 69, 80, 73]
proportions = []
for index in range(len(w)):
    prop_item = round(w[index] / h[index] ,1)
    proportions.append(prop_item)
x = list(range(len(proportions)))
plt.figure(figsize=(10, 6))
plt.plot(x, proportions, marker='o', color='b', linestyle='-')

# Добавление заголовков и подписей осей
plt.title('График по точкам')
plt.xlabel('Индекс')
plt.ylabel('Значение')

# Отображение графика
plt.grid(True)
plt.show()