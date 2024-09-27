import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from future.moves import sys

from FinalHandler import FinalHandler
from Reader import Reader
from ViewTrack import ViewTrack
from configs import config
from player import MainWindow


class ButtonsHandler(MainWindow):
    def __init__(self):
        super().__init__()
        self.connect_buttons()
        self.check_for_filling_of_data()

    def open_error_corrector(self, checked):
        if self.ErrorCorrector.isVisible():
            self.ErrorCorrector.hide()
        else:
            self.ErrorCorrector.show()

    def open_view_track(self):
        if self.ViewTrack.isVisible():
            self.ViewTrack.hide()
        else:
            self.ViewTrack.show()

    def choose_geojson(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        save_path, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                   "geojson (*.geojson)", options=options)
        if save_path not in ".geojson":
            save_path += ".geojson"
        config.PATH_TO_GEOJSON = save_path
        self.label_geojson.setText("{}".format(config.PATH_TO_GEOJSON))
        self.check_for_filling_of_data()

    def choose_GPX(self):
        gpx_path = QtWidgets.QFileDialog.getOpenFileName(filter="gpx (*.gpx)")

        config.PATH_TO_GPX = gpx_path[0].replace('/', '\\')
        if config.PATH_TO_GPX == "":
            self.label_gpx.setText("<font color=black>" + "Пустой GPX" + "</font>")
        else:
            self.Reader = Reader(config.PATH_TO_GPX)
            self.label_gpx.setText("<font color=black>" + str(config.PATH_TO_GPX) + "</font>")
        self.check_for_filling_of_data()

    def check_for_filling_of_data(self):
        is_filled_all = len(config.PATH_TO_GEOJSON) > 3 and len(config.PATH_TO_GPX) > 3 and len(config.PATH_TO_VIDEO) > 3
        self.button_treatment.setEnabled(is_filled_all)
        self.button_corrector.setEnabled(is_filled_all)
        self.button_viewTrack.setEnabled(is_filled_all)
        if is_filled_all:
            self.ViewTrack = ViewTrack()
            self.finalHandler = FinalHandler()
    def choose_dir(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        config.PATH_TO_VIDEO = dirlist.replace('/', '\\') + "\\"
        config.VIDEOS = os.listdir(config.PATH_TO_VIDEO)

        self.label_dir.setText("{}".format(config.PATH_TO_VIDEO))
        self.Files = dirlist
        self.check_for_filling_of_data()

    def connect_buttons(self):
        self.button_corrector.clicked.connect(self.open_error_corrector)
        self.button_viewTrack.clicked.connect(self.open_view_track)
        self.button_choose_geojson.clicked.connect(self.choose_geojson)
        self.button_choose_GPX.clicked.connect(self.choose_GPX)
        self.button_choose_dir.clicked.connect(self.choose_dir)


