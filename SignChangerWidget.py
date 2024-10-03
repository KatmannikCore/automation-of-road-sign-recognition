from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QCheckBox, QLineEdit

from ModalWindowChanger import ModalWindowChanger
from configs.sign_config import type_signs_with_text


class SignChangerWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.button_change_type = QPushButton("Изменить тип", self)
        self.button_change_type.move(1000, 55)
        self.button_change_type.clicked.connect(self.open_change_type_window)

        self.button_delete = QPushButton("Удалить", self)
        self.button_delete.move(1000, 150)

        self.ModalWindowChanger = ModalWindowChanger()

        self.ModalWindowChanger.list_widget.itemClicked.connect(self.change_type)

        self.label_t = QLabel('Тип:', self)
        self.label_t.setGeometry(1000, 35, 1000, 20)

        self.label_img_type = QLabel(self)
        self.img_type = QPixmap()

        self.label_img_type.setPixmap(self.img_type)
        self.label_img_type.resize(100, 100)
        self.label_img_type.move(1090, 0)

        self.label_type = QLabel('name', self)
        self.label_type.setGeometry(1025, 35, 1000, 20)

        self.checkbox_side = QCheckBox("Боковой", self)
        self.checkbox_side.move(1000, 85)

        self.label_dir = QLabel('Текст', self)
        self.label_dir.setGeometry(1000, 105, 1000, 20)

        self.textbox_text = QLineEdit(self)
        self.textbox_text.move(1040, 105)
        self.textbox_text.resize(80, 20)

        self.current_index = 0

    def set_sing(self, feature):
        self.label_type.setText(feature["properties"]['type'])
        self.img_type = QPixmap(rf"./sings/V{feature['properties']['type']}.png")
        self.label_img_type.setPixmap(self.img_type)
        self.checkbox_side.setChecked(feature["properties"]['side'] == "True")

    def toggle_textbox(self, feature):
        is_contain_text = feature["properties"]['type'] in type_signs_with_text
        self.textbox_text.setEnabled(is_contain_text)
        self.textbox_text.setText(feature["properties"]["MVALUE"] if is_contain_text else "")

    def open_change_type_window(self):
        if self.ModalWindowChanger.isVisible():
            self.ModalWindowChanger.hide()
        else:
            self.ModalWindowChanger.show()

    def change_type(self, item):
        type_of_sing = item.text().replace("V", "")
        self.label_type.setText(type_of_sing)
        self.img_type = QPixmap(rf"./sings/{item.text()}.png")
        self.label_img_type.setPixmap(self.img_type)
        self.textbox_text.setEnabled(type_of_sing in type_signs_with_text)
        self.ModalWindowChanger.hide()
