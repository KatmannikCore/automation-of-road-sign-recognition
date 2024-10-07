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
rename_files("D:\sings")




