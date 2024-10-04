import os

import geojson

from configs import config


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


with open(rf"D:\Urban\vid\test\city1.geojson", encoding='utf-8') as f:
  data = geojson.load(f)["features"]
  new_object = {}
  coordinates = []
  azimuth = []
  types = []
  for item in data:
   coordinates.append(item["geometry"]["coordinates"])
   azimuth.append(float(item["properties"]["azimuth"]))
   types.append(item["properties"]["type"])
  new_object["coordinates"] = coordinates
  new_object["azimuth"] = azimuth
  new_object["types"] = types

print(new_object)