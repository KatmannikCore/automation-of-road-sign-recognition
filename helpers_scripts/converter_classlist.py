dict_old = {
    0:"parkovka",
    1:"iskusstvennaya nerovnost",
    2:"ogranichenie skorosti",
    3:"glavnaya doroga",
    4:"peshehodnyj perehod",
    5:"ostanovka i parkovka zapreshena",
    6:"dvizhenie gruzovogo transporta",
    7:"napravlenie dvizheniya po polosam",
    8:"ustupi dorogu",
    9:"kirpich",
    10:"suzhenie dorogi",
    11:"Obgon zarashyon",
    12:"STOP",
    13:"dvizhenie pryamo",
    14:"ostanovka avtobusov",
    15:"deti",
    16:"tablichka |",
    17:"tablichka __",
    18:"obezd prepyatstviya <",
    19:"obezd prepyatstviya >",
    20:"obezd prepyatstviya <>",
    21:"dvizhenie peshehoda zapresheno",
    22:"polosa dlya obshestvennogo transporta",
    23:"dvizhenie zapresheno",
    24:"dvizhenie velosipedov zapresheno",
    25:"doroga s odnostoronnim dvizheniem",
    26:"ostanovka avtobusa tablichka",
    27:"opasnyj povorot >",
    28:"opasnyj povorot <",
    29:"opasnye povoroty |\|",
    30:"opasnye povoroty |/|",
    31:"napravlenie glavnoj dorogi",
    32:"konec zony ogranicheniya max skorosti",
    33:"dvizhenie napravo >",
    34:"dvizhenie nalevo <",
    35:"povorot zapreshen >",
    36:"povorot zapreshen <",
    37:"zapravka",
    38:"avtomojka",
    39:"CTO",
    40:"Nachalo polosy (pravo)",
    41:"Nachalo polosy (levo)",
    42:"Konec polosy (pravo)",
    43:"Konec polosy (levo)",
    44:"vperedi velosipednyj proezd",
    45:"Dvizenie |-",
    46:"razvorod",
    47:"sbros ogranichenij",
    48:"ostanovka taksi",
    49:"opasnyj uchastok",
    50:"konec odnostoronnego dvizheniya",
    51:"napravlenie dvizenia gruzovix avtomobilei",
    52:"STOP tablichka",
    53:"tupik",
    54:"razvorot zapreshen",
    55:"zhilaya zona",
    56:"konec glavnaya doroga",
    57:"zhd bez --",
    58:"primikanie vrotostepennoy dorogi",
    59:"viezd na dorogu s odnostorinnim dvizeniem >",
    60:"dvustornnie dvizenie",
    61:"hostel",
    62:"ogranichenie height",
    63:"ogranichenie width",
    64:"zhd s --",
    65:"konec zhilaya zona",
    66:"ostanovochnuy punkt tramvaya",
    67:"mesto ostanovki tramvaya",
    68:"hospital",
    69:"Dvizenie -|",
    70:"Tyalet",
    71:"Krugovoe dvijenie",
    72:"konec polosu dlya obshestvennogo transporta",
    73:"Avariuno opasnuy ychastok",
    74:"Zona otduha",
    75:"Xavka",
    76:"Ogranichenie Minimalnogo Rastoyania",
    77:"Platnaya Doroga"
}
dict_new = {
    "parkovka":0,
    "iskusstvennaya nerovnost":1,
    "ogranichenie skorosti":2,
    "glavnaya doroga":3,
    "peshehodnyj perehod":4,
    "ostanovka i parkovka zapreshena":5,
    "viezd na dorogu s odnostorinnim dvizeniem >":6,
    "napravlenie dvizheniya po polosam":7,
    "ustupi dorogu":8,
    "kirpich":9,
    "zhilaya zona":10,
    "tupik":11,
    "STOP":12,
    "dvizhenie pryamo":13,
    "ostanovka avtobusov":14,
    "konec odnostoronnego dvizheniya":15,
    "tablichka |":16,
    "tablichka __":17,
    "obezd prepyatstviya <":18,
    "obezd prepyatstviya >":19,
    "obezd prepyatstviya <>":20,
    "Dvizenie |-":21,
    "polosa dlya obshestvennogo transporta":22,
    "dvizhenie napravo >":23,
    "napravlenie glavnoj dorogi":24,
    "doroga s odnostoronnim dvizheniem":25,
    "ostanovka avtobusa tablichka":26,
    "Krugovoe dvijenie":27,
    "Recomenduemaya ckorost":28,
    "Dvizenie_napravo_ili_nalevo":29,
    "konec zhilaya zona":30,
    "dvizhenie nalevo <":31,
    "Priemuchectvo pered vstrechnum dvicheniem":32,
    "konec polosu dlya obshestvennogo transporta":33
}
import os
import shutil
directory = r'D:\Ur2\rezerv\smail\txt'
desired_digit = None
new_directory = r'C:\Users\Urbanovich\OneDrive\Рабочий стол\Егорыч не трогай\smail\txt'
directoryImg = r'C:\Users\Urbanovich\OneDrive\Рабочий стол\Егорыч не трогай\img'
new_directoryImg = r'C:\Users\Urbanovich\OneDrive\Рабочий стол\Егорыч не трогай\smail\img'

dict = {'0': 38, '1': 21, '14': 40, '17': 228, '18': 24, '19': 108, '2': 139, '20': 53, '25': 59, '26': 12, '3': 172, '31': 268, '32': 20, '33': 47, '34': 181, '4': 768, '47': 21, '5': 44, '50': 19, '51': 70, '53': 2, '55': 29, '56': 116, '59': 22, '65': 60, '67': 64, '69': 43, '7': 316, '71': 219, '72': 12, '77': 47, '8': 395, '9': 81}


for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r') as file:
        lines = file.readlines()
    with open(filepath, 'w') as file:
        for line in lines:
            number = line.split(" ")[0]
            line = line.replace(str(number), "konec polosu dlya obshestvennogo transporta", 1)
            file.write(line)
#for filename in os.listdir(directory):
#    filepath = os.path.join(directory, filename)
#    with open(filepath, 'r') as file:
#        lines = file.readlines()
#    with open(filepath, 'w') as file:
#        for line in lines:
#            number = int(line.split(" ")[0])
#            if number != dict_new.get(dict_old.get(number)):
#                print(number, dict_old.get(number), dict_new.get(dict_old.get(number)))
#            file.write(line)