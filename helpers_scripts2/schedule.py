import matplotlib.pyplot as plt

data = [22, 25, 26, 25, 25, 25, 27, 26, 29, 29, 32, 31, 32, 36, 41, 42, 46, 47, 48, 50]
plt.plot(data, marker='o')
plt.title('График данных')
plt.xlabel('Номер элемента')
plt.ylabel('Значение')
plt.show()