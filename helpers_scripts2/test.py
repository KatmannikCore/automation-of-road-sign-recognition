import os

# Получаем список всех файлов и папок в текущей директории
content = os.listdir(r'D:\Urban\yolov4\yolov4-opencv-python\train\blue\\')

# Фильтруем только папки
folders = [f for f in content if os.path.isdir(f)]

# Выводим имена папок
for folder in content:
    print(folder)