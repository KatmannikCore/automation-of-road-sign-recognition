import numpy as np
import matplotlib.pyplot as plt

# Задаем данные для точек графика
X = np.array([1458, 1500, 1545, 1595, 1653, 1712, 1785])
Y = np.array([ 631, 618, 603, 584, 562, 529, 502])

X = np.array([1881, 1845, 1803, 1768, 1729, 1684, 1643, 1611, 1582, 1575, 1570, 1577, 1598, 1641, 1695 ])
Y = np.array([456, 453, 441, 437, 435, 428, 414, 405, 380, 365, 327, 290, 234, 171, 87  ])

# Производим аппроксимацию линейной функцией (y = mx + c) с помощью метода наименьших квадратов
A =   np.vstack([X, np.ones(len(X))]).T
m, c = np.linalg.lstsq(A, Y, rcond=None)[0]

# Выводим значение найденных коэффициентов
print("Коэффициенты: m =", m, "c =", c)

# Строим график с использованием точек и аппроксимирующей функции
plt.scatter(X, Y, label='Точки графика')
plt.xlabel('Значения по оси X')
plt.ylabel('Значения по оси Y')
plt.title('Аппроксимация точек графика')
plt.legend()
plt.show()
