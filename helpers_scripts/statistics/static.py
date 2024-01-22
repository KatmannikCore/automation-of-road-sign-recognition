def convert_YOLO_to_normal(new_line):
    x_center = float(new_line[1]) * 1920.0
    y_center = float(new_line[2]) * 1080.0
    x_width = (float(new_line[3]) * 1920.0) / 2.0
    y_height = (float(new_line[4]) * 1080.0) / 2.0
    xmin = int(round(x_center - x_width))
    ymin = int(round(y_center - y_height))
    xmax = int(round(x_center + x_width))
    ymax = int(round(y_center + y_height))
    h = ymax - ymin
    w = xmax - xmin
    return h, w
classifier = [
            "parkovka",
            "treugolnik",
            "krug",
            "glavnaya doroga",
            "peshehodnyj perehod",
            "ostanovka i parkovka zapreshena",
            "viezd na dorogu s odnostorinnim dvizeniem >",
            "napravlenie dvizheniya po polosam",
            "ustupi dorogu",
            "red",
            "zhilaya zona",
            "tupik",
            "polosa dlya obshestvennogo transporta",
            "blue",
            "servises",
            "konec odnostoronnego dvizheniya",
            "tablichka |",
            "tablichka __",
            "ostanovka avtobusa tablichka",
            "doroga s odnostoronnim dvizheniem",
            "napravlenie glavnoj dorogi",
            "nachalo nas punkta bel s dom",
            "konec nas punkta bel s dom",
            "nachalo nas punkta bel",
            "konec nas punkta bel",
            "nachalo nas punkta sin",
            "konec nas punkta sin",
            "Sbros vseh ogranicheniu",
            "platnaua doroga"
        ]