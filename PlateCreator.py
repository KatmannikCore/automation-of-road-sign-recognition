import json

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QVBoxLayout

from configs.sign_config import plate_for_signatures


class PlateCreator(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 240, 240)
        self.path_to_signs = "./signs.json"
        self.list_widget = QListWidget()
        self.list_widget.setIconSize(QSize(50, 50))  # Размер иконок
        self.crate_type_boxes()
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)
        self.list_widget.setViewMode(QListWidget.IconMode)  # Устанавливаем режим отображения иконок
        self.list_widget.setResizeMode(QListWidget.Adjust)  # Автоматическое изменение размера
        self.list_widget.setFlow(QListWidget.LeftToRight)  # Устанавливаем направление потока
        self.list_widget.setSpacing(5)  # Задаем отступ между элементами
        self.list_widget.setGridSize(QSize(65, 65))  # Размер ячейки сетки

    def crate_type_boxes(self):
        for type in plate_for_signatures:
            pixmap = QPixmap(fr"./sings/V{type}.png")
            icon = QIcon(pixmap)
            item_list = QListWidgetItem(icon, type)
            self.list_widget.addItem(item_list)


