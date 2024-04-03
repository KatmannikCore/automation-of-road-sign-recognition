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
        prop_max = round(max(h) / max(w), 2)
        prop_min = round(min(h) / min(w), 2)
        prop_h = round(h[-1] /h[0], 2)
        prop_w = round(w[-1] /w[0], 2)
        #print(f"Name: {name_one} max: {prop_max} min: {prop_min} h: {prop_h} w:{prop_w}")
        if 100 > max(h):
            print(item)