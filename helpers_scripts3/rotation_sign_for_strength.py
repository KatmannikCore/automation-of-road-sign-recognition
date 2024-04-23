import json
file_path = 'sample.json'
from termcolor import colored


def split_array( arr):
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    return left, right


with open(file_path, 'r') as file:
    # Загружаем данные из JSON файла
    data = json.load(file)['objects']
    for item in data:

        name_one = item['name_one']
        name_two = item['name_two']

        w = item['w']
        h = item['h']
        x = item['x']
        y = item['y']

        length = item['length']
        if length < 4:
            continue
        number = item['number'] - 63600
        if number > 63600:
            number = number - 63600
        frame = round(number / 60, 0)
        minute = int(frame / 60)
        part_seconds = (frame / 60 ) - minute
        seconds = int(60 * part_seconds)
        max_w = max(w)
        max_h = max(h)
        min_w = min(w)
        min_h = min(h)
        names_signs_for_side = ["parkovka", "ostanovka i parkovka zapreshena", "krug", "red", "tupik", "zhilaya zona",
                                "red"]
        CS = (max_w * max_h) / (min_h * min_w)
        proportions = [w[index] / h[index] for index in range(len(h))]
        left_half, right_half = split_array(proportions)
        if not left_half:
            continue

        different_left = abs(min(left_half) - max(left_half))
        different_right = abs(min(right_half) - max(right_half))
        average = sum(proportions) / len(proportions)



        if  CS < 10 and \
            (max_w * max_h) < 20500 and \
            x[0] > 1000 and \
            len(w) >= 4 and \
            name_one in names_signs_for_side and \
            (different_left > different_right or average < 0.9):

                print(f"Time: {minute}.{seconds}")
                print(item)

