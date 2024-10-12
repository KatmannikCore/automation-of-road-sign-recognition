#! /usr/bin/env python
# -*- coding: utf-8 -*-
def remove_large_numbers(file_path):
    try:
        new_arr = []
        # Читаем содержимое файла
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line = line.replace("\t", "").replace("\n", "").strip().replace("V", "")
                new_arr.append(line)
        arr = new_arr
        result = {}
        for i in range(len(arr) - 1):
            if  i % 2 == 0:
                result[arr[i + 1]] = arr[i]
        print(result)
    except Exception as e:
        print(f"Произошла ошибка: {e}")


# Укажите путь к вашему текстовому файлу
file_path = '1.txt'
remove_large_numbers(file_path)
