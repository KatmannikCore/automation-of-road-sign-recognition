import xml.etree.ElementTree as ET
import os

# задаём путь к директории с gpx-файлами
dir_path = './'

# перебираем все файлы в директории
for filename in os.listdir(dir_path):
    if filename.endswith('.gpx'):
        # открываем файл gpx-файла
        tree = ET.parse(os.path.join(dir_path, filename))

        # получаем корневой элемент
        root = tree.getroot()

        # ищем все теги trkpt
        trkpts = root.findall(".//{http://www.topografix.com/GPX/1/1}trkpt")

        # выводим количество найденных тегов
        print("Файл:", filename)
        print("Количество тегов trkpt:", len(trkpts))