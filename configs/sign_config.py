from tensorflow.keras.models import load_model
model_dict = {
    "blue": load_model(r'./models_200_10/blue.h5'),
    "treugolnik": load_model(r'./models_200_10/treugolnik.h5'),
    "krug": load_model(r'./models_200_10/krug.h5'),
    "red": load_model(r'./models_100/red.h5'),
    "servises": load_model(r'./models_200_10/servises.h5'),
    "tablichka __": load_model(r'./models_200_10/tab.h5'),
    "tablichka |": load_model(r'./models_200_10/tabl l.h5'),
    "tupik": load_model(r'./models_200_10/tupik.h5')
}
sub_models = {
    'danger': load_model(r'./models_200_10/treugolnik/danger.h5'),
    'pimicanie': load_model(r'./models_200_10/treugolnik/pimicanie.h5'),
    'suzenie': load_model(r'./models_200_10/treugolnik/suzenie.h5')
}

model = load_model(r'./test_c171_r10_e80.h5')

name_signs_cnn = {
    "blue": ["4.1.4", "4.3","4.2.2", "4.1.6", "4.1.3", "4.1.1", "4.1.4", "0000010420", "4.2.1","4.1.2"],
    "krug": ["3.2", "3.24", "3.18.2", "3.13", "3.5", "3.4", "3.20.1",  "empty", "3.18.1", "3.9"],
    "red": ["2.5","3.1"],
    "treugolnik": ["1.21", "1.23", "1.29", "1.8", "1.17", "suzenie","1.32", "1.5", "pimicanie", "danger"],
    "servises": ["5.16", "7.1", "7.3", "7.5", "7.4", "7.11", "7.18", "7.2", "5.14.2", "7.15", "7.7", "6.12.2", "7.16"],
    "tablichka __" : ["8.12", "8.3.1",  "8.8", "8.10", "8.2.6", "8.2.1", "8.3.2", "8.5.7", "8.1.3", "7.14.1", "8.1.1", "8.15" ],
    "tablichka |" : ["8.2.4", "8.2.3", "8.2.2"],
    "tupik" : ["6.8.1", "5.19.3", "6.8.2"]
}
name_sub_signs_cnn = {
    "danger": ['1.11.2', '1.11.1', '1.12.2'],
    "pimicanie": ['2.3.3', '2.3.2', '2.3.1'],
    "suzenie":['1.20.2','1.20.3','1.20.2']
}

type_signs_yolo = {
    "parkovka": "6.4",
    "glavnaya doroga": "2.1",
    "peshehodnyj perehod": "5.16.2",
    "ostanovka i parkovka zapreshena": "3.27",
    "napravlenie dvizheniya po polosam" : "5.8.1",
    "ustupi dorogu" : "2.4",
    "zhilaya zona" : "5.38",
    "polosa dlya obshestvennogo transporta" : "5.9.1",
    "konec odnostoronnego dvizheniya" : "5.6",
    "ostanovka avtobusa tablichka" : "5.16",
    "doroga s odnostoronnim dvizheniem" : "5.5",
    "napravlenie glavnoj dorogi" : "7.13.1",
    "Sbros vseh ogranicheniu" : "3.31",
    "viezd na dorogu s odnostorinnim dvizeniem >": "5.7.2",
    "nachalo nas punkta bel s dom" : "5.22.2",
    "konec nas punkta bel s dom" : "5.23.2",
    "nachalo nas punkta bel" : "5.22.1",
    "konec nas punkta bel" : "5.23.1",
    "nachalo nas punkta sin" : "5.23.3",
    "konec nas punkta sin" : "5.25.3",
    "platnaua doroga" : "7.17"
}

type_signs_with_text = ['3.24', '3.11', '3.12', '3.13', '3.14', '3.15', '8.1.4', '8.1.3', '8.2.1', '8.2.2', '8.2.5', '8.2.6', '7.1.2', '7.7.1', '8.1.1', '7.9.1']
name_signs_city = [ "nachalo nas punkta bel s dom", "konec nas punkta bel s dom", "nachalo nas punkta bel", "konec nas punkta bel", "nachalo nas punkta sin", "konec nas punkta sin"]
names_signs_for_side = ["parkovka", "ostanovka i parkovka zapreshena", "krug", "red", "tupik", "zhilaya zona", "red"]
names_signs_for_YOLO = ["parkovka","treugolnik","krug","glavnaya doroga","peshehodnyj perehod","ostanovka i parkovka zapreshena","viezd na dorogu s odnostorinnim dvizeniem >","napravlenie dvizheniya po polosam","ustupi dorogu","red","zhilaya zona","tupik","polosa dlya obshestvennogo transporta","blue","servises","konec odnostoronnego dvizheniya","tablichka |","tablichka __","ostanovka avtobusa tablichka","doroga s odnostoronnim dvizheniem","napravlenie glavnoj dorogi","nachalo nas punkta bel s dom","konec nas punkta bel s dom","nachalo nas punkta bel","konec nas punkta bel","nachalo nas punkta sin","konec nas punkta sin","Sbros vseh ogranicheniu","platnaua doroga"]