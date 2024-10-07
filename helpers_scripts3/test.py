import tensorflow as tf
import numpy as np

# Пример данных
data = [
    {"name_one": "red", "name_two": "3.1", "w": [29, 30, 23, 22, 24, 32, 31, 35, 38, 40, 40, 44, 54, 30],"h": [31, 31, 46, 46, 50, 63, 62, 57, 59, 73, 64, 72, 85, 84],"x": [1115, 1122, 1525, 1549, 1574, 1596, 1627, 1659, 1689, 1724, 1765, 1803, 1841, 1890],"y": [624, 621, 554, 548, 539, 525, 520, 517, 508, 493, 485, 469, 450, 440], "length": 14, "number": 256005},
    {"name_one": "krug", "name_two": "3.2", "w": [35, 44, 40, 48, 36], "h": [52, 49, 54, 67, 50], "x": [1679, 1740, 1811, 1843, 1884], "y": [524, 522, 514, 499, 495]},
    {"name_one": "krug", "name_two": "3.2", "w": [29, 31, 43, 37, 46, 46, 50, 55, 58, 36], "h": [46, 57, 53, 61, 57, 61, 77, 68, 86, 77], "x": [1453, 1507, 1568, 1602, 1639, 1680, 1722, 1776, 1824, 1884], "y": [497, 476, 451, 437, 427, 412, 384, 365, 335, 319]},
    {"name_one": "ostanovka i parkovka zapreshena", "name_two": "3.27", "w": [24, 29, 29, 31, 32, 34, 28, 39, 37, 40, 36], "h": [40, 35, 36, 46, 51, 40, 45, 56, 49, 57, 53], "x": [1585, 1623, 1645, 1668, 1694, 1721, 1759, 1779, 1813, 1847, 1884], "y": [605, 601, 597, 586, 581, 581, 573, 561, 559, 548, 542]}
]

# Преобразование данных в формат NumPy
names = [d["name_one"] for d in data]
w = np.array([d["w"] for d in data], dtype=object)
h = np.array([d["h"] for d in data], dtype=object)
x = np.array([d["x"] for d in data], dtype=object)
y = np.array([d["y"] for d in data], dtype=object)

# One-hot encoding для имен
unique_names = list(set(names))
name_to_index = {name: index for index, name in enumerate(unique_names)}
name_encoded = np.array([name_to_index[name] for name in names])
name_one_hot = tf.keras.utils.to_categorical(name_encoded)



# Находим максимальную длину последовательности
max_len = max(len(arr) for arr in w)

# Добавляем нули в короткие последовательности для выравнивания длины
w_padded = np.array([np.pad(arr, (0, max_len - len(arr)), 'constant') for arr in w])
h_padded = np.array([np.pad(arr, (0, max_len - len(arr)), 'constant') for arr in h])
x_padded = np.array([np.pad(arr, (0, max_len - len(arr)), 'constant') for arr in x])
y_padded = np.array([np.pad(arr, (0, max_len - len(arr)), 'constant') for arr in y])

# Нормализация числовых данных
w_norm = w_padded / np.max(w_padded)
h_norm = h_padded / np.max(h_padded)
x_norm = x_padded / np.max(x_padded)
y_norm = y_padded / np.max(y_padded)

# Объединение данных
data_norm = np.stack((w_norm, h_norm, x_norm, y_norm), axis=2)

# Разделение данных на обучающий и тестовый наборы
train_data, test_data = data_norm[:2], data_norm[2:]
train_labels, test_labels = name_one_hot[:2], name_one_hot[2:]

# Создание модели
model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(128, input_shape=(data_norm.shape[1], data_norm.shape[2])),
    tf.keras.layers.Dense(len(unique_names), activation='softmax')
]) 

# Компиляция модели
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Обучение модели
model.fit(train_data, train_labels, epochs=10)

# Оценка модели
loss, accuracy = model.evaluate(test_data, test_labels)
print('Loss:', loss)
print('Accuracy:', accuracy)

# Предсказание
predictions = model.predict(test_data)