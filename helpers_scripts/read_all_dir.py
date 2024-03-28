import os
path = r'D:\Urban\yolov4\yolov4-opencv-python\train\treugolnik'

# Получаем список всех элементов в директории
content = os.listdir(path)

# Фильтруем только папки
folders = [f for f in content if os.path.isdir(os.path.join(path, f))]

# Выводим список всех папок
for folder in folders:
    print(folder)