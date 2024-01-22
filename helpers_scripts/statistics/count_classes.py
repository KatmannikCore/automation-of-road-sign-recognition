import os
path_classlist = r""
path_txt = r"E:\recognition_sings\NaselennuePunkty\YOLO_darknet"
counter_list = {}
classes= [
    "parkovka",
    "iskusstvennaya nerovnost",
    "ogranichenie skorosti",
    "glavnaya doroga",
    "peshehodnyj perehod",
    "ostanovka i parkovka zapreshena",
    "viezd na dorogu s odnostorinnim dvizeniem >",
    "napravlenie dvizheniya po polosam",
    "ustupi dorogu",
    "kirpich",
    "zhilaya zona",
    "tupik",
    "STOP",
    "dvizhenie pryamo",
    "ostanovka avtobusov",
    "konec odnostoronnego dvizheniya",
    "tablichka |",
    "tablichka __",
    "obezd prepyatstviya <",
    "obezd prepyatstviya >",
    "obezd prepyatstviya <>",
    "Dvizenie |-",
    "polosa dlya obshestvennogo transporta",
    "dvizhenie napravo >",
    "napravlenie glavnoj dorogi",
    "doroga s odnostoronnim dvizheniem",
    "ostanovka avtobusa tablichka",
    "Krugovoe dvijenie",
    "Recomenduemaya ckorost",
    "Dvizenie napravo ili nalevo",
    "konec zhilaya zona",
    "dvizhenie nalevo <",
    "konec polosu dlya obshestvennogo transporta",
    "nachalo nas punkta bel ",
    "konec nas punkta bel ",
    "nachalo nas punkta sin ",
    "konec nas punkta sin ",
    "Sbros vseh ogranicheniu",
    "platnaua doroga"
]
numbers = {0: 170, 1: 235, 2: 259, 3: 296, 4: 1508, 5: 569, 6: 9, 7: 418, 8: 462, 9: 119, 10: 19, 11:0, 12: 16, 13: 136, 14: 288, 15: 66, 16: 76, 17: 465, 18: 22, 19: 57, 20: 45, 21: 18, 22:0, 23: 25, 24: 50, 25: 45, 26: 0, 27: 0, 28:0, 29:0, 30: 13, 31:0, 32:0, 33:0}


#arr = [[classes[item], numbers[item] ,item] for item in range(len(classes)) ]
#for item in arr:
#     print(item)
for filename in os.listdir(path_txt):
    filepath = os.path.join(path_txt, filename)
    with open(filepath, 'r') as file:
        lines = file.readlines()
        for line in lines:
            number = int(line.split(" ")[0])
            if not counter_list.get(number):
                counter_list.update({number: 0})
            counter_list[number] +=1

counter_list = dict(sorted(counter_list.items()))
print(counter_list)