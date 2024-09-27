import sys
from PyQt5.QtWidgets import QApplication
from ButtonsHandler import ButtonsHandler


class ViewPlayer(ButtonsHandler):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ViewPlayer()
    sys.exit(app.exec_())
