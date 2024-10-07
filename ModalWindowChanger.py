import json
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QVBoxLayout


class ModalWindowChanger(QWidget):
    def __init__(self):
        super().__init__()

        # Создание списка
        self.selected_element = None
        self.list_widget = QListWidget()
        self.list_widget.setIconSize(QSize(200, 200))  # Размер иконок
        self.setGeometry(200, 200, 800, 800)
        self.path_to_signs = "./signs.json"

        # Добавление изображений
        self.crate_type_boxes()
        # Вертикальный layout
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

        # Установка количества колонок в списке
        self.list_widget.setViewMode(QListWidget.IconMode)  # Устанавливаем режим отображения иконок
        self.list_widget.setResizeMode(QListWidget.Adjust)  # Автоматическое изменение размера
        self.list_widget.setFlow(QListWidget.LeftToRight)  # Устанавливаем направление потока
        self.list_widget.setSpacing(10)  # Задаем отступ между элементами
        self.list_widget.setGridSize(QSize(120, 120))  # Размер ячейки сетки

    def crate_type_boxes(self):
        with open(self.path_to_signs, 'r', encoding='utf-8') as f:
            data = json.load(f)['MapLegend']
            for class_name in data:
                for items in data[class_name]['Item']:
                    self.add_image(fr"./sings/{items['_Image']}", items['_Key'])
    def add_image(self, image_path, text):
        """Добавляет изображение в список."""
        # Загрузка изображения
        pixmap = QPixmap(image_path)
        icon = QIcon(pixmap)
        # Создание элемента списка
        item = QListWidgetItem(icon, text)
        # Добавление элемента в список
        self.list_widget.addItem(item)


