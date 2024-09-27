from player import MainWindow


class PlayerHandler(MainWindow):
    def open_error_corrector(self, checked):
        if self.ErrorCorrector.isVisible():
            self.ErrorCorrector.hide()
        else:
            self.ErrorCorrector.show()

