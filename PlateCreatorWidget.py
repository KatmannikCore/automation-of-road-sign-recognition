from PyQt5.QtWidgets import QWidget, QPushButton


class PlateCreatorWidget(QWidget):
    def __init__(self,   parent=None):
        self.button_delete_plate = QPushButton("Удалить табличку", self)
        self.button_delete_plate.move(1000, 300)
