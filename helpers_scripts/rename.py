
import os
import random
import string

def random_string(count):
    return ''.join(str(count))

def rename_files(directory):
    count = 0
    for path, subdirs, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(path, name)
            new_file_name = 'a' + random_string(count) + os.path.splitext(name)[1]
            new_file_path = os.path.join(path, new_file_name)
            os.rename(file_path, new_file_path)
            count +=1
            print(f'{file_path} renamed to {new_file_path}')

# Пример использования

rename_files(r'D:\Ur2\test10\39а')