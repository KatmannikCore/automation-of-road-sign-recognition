import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from FinalHandler import FinalHandler
from PlayerHandler import PlayerHandler
from Reader import Reader
from ViewTrack import ViewTrack
from configs import config



class ButtonsHandler(PlayerHandler):
    def __init__(self):
        super().__init__()
       # self.playerHandle = PlayerHandler()
        self.connect_buttons()
        self.check_for_filling_of_data()


    def open_error_corrector(self, checked):
        if self.errorCorrector.isVisible():
            self.errorCorrector.hide()
        else:
            self.errorCorrector.show()

    def open_view_track(self):
        if self.viewTrack.isVisible():
            self.viewTrack.hide()
        else:
            self.viewTrack.show()

    def choose_geojson(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        save_path, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                   "geojson (*.geojson)", options=options)
        if save_path.find(".geojson") == -1 and len(save_path) != 0:
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
            self.viewTrack = ViewTrack()
            self.finalHandler = FinalHandler()
    def choose_dir(self):
        #TODO фильтр mp4 файлов
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
        self.button_treatment.clicked.connect(self.start_processing)
        self.button_end.clicked.connect(self.finish_processing)

