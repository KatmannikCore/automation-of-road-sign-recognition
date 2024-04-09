import json
file_path = 'sample.json'
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
        number = item['number']
        CS = round ((max(w) * max(h)) / (min(w) * max(h)), 1)
        #print(f"Name: {name_one} max: {prop_max} min: {prop_min} h: {prop_h} w:{prop_w}")
        if  CS < 10 and (max(w) * max(h)) < 20000 and x[0] > 1000:
            frame = round(number / 60, 0)
            minute = int(frame / 60)
            part_seconds = (frame / 60) - minute
            seconds = int(60 * part_seconds)
            print(f"Time: {minute}.{seconds}")
            print(max(w) * max(h), min(w) * max(h))
            print(f"CS: {CS}")
            print(item)
            print("____________")