import os
import gpxpy
import gpxpy.gpx

from configs import config

import xml.etree.ElementTree as ET
def rename_files(directory):
 """Переименовывает все файлы в указанном каталоге, добавляя "V" в начало имени."""

 for filename in os.listdir(directory):
  # Пропускаем файлы, которые не являются обычными файлами
  if os.path.isfile(os.path.join(directory, filename)):
   old_path = os.path.join(directory, filename)
   new_path = os.path.join(directory, "V" + filename)
   os.rename(old_path, new_path)
   print(f"Переименовано: {filename} -> {new_path}")


# Замените "путь/к/каталогу" на фактический путь к каталогу, который нужно обработать
#rename_files("D:\sings")





with open(rf"D:\Urban\vid\test\GOPR0083.gpx", 'r')as f:
    count = 10
    gpx = gpxpy.parse(f)
    point = gpx.tracks[0].segments[0].points[0]
    #for index in range(count):
    #    print(gpx)

import xml.etree.ElementTree as ET

ET.register_namespace("", "https://www.gpsbabel.org")
ET.register_namespace("", "http://www.topografix.com/GPX/1/0")

gpx_file = r'D:\Urban\vid\test\GOPR0083.gpx'
tree = ET.parse(gpx_file)
root = tree.getroot()


def add_point_to_gpx(count_poinst):
    coordinates = root[2][0][0].attrib
    properties = root[2][0][0]
    # Создаем новую точку
    trkpt = create_new_trkpt(coordinates, properties)
    for index in range(count_poinst):
        root[2][0].insert(0, trkpt)
    # Сохраняем изменения в файл
    tree.write(rf"D:\1.gpx", encoding='utf-8', xml_declaration=True)

def remove_first_trkpt(cound_delete_points):
    # Ищем первый элемент <trkpt> и удаляем его
    for index in range(cound_delete_points):
        trkpt = root[2][0][index]
        if trkpt is not None: # Получаем родительский элемент
            root[2][0].remove(trkpt)  # Удаляем первую точку

    # Сохраняем изменения в файл
    tree.write(rf"D:\1.gpx", encoding='utf-8', xml_declaration=True)

number_ofset = -1
if number_ofset > 0:
    add_point_to_gpx(0)
else:
    remove_first_trkpt(10)