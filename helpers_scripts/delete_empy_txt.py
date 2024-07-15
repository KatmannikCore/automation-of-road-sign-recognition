import os

"""
Удаляет все пустые текстовые файлы в заданной папке.
"""
def del_empty_files(dirs):
    for dir in os.listdir(dirs):
      dir = f"{dirs}\\{dir}"
      for filename in os.listdir(dir):
        filepath = os.path.join(dir, filename)
        if os.path.isfile(filepath) and filename.endswith(".txt"):
          with open(filepath, "r", encoding="utf-8") as f:
            if os.stat(filepath).st_size == 0:
              f.close()
              os.remove(filepath)
              path_img = filepath.replace('txt','jpg')
              os.remove(path_img)
              print(f"Удален пустой файл: {filename} и {path_img}")

# Пример использования
dir = r"D:\123"  # Замените на путь к вашей папке
del_empty_files(dir)