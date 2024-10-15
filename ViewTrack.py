from threading import Thread

from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QPushButton, QMainWindow

from Server import Server
from VideoWidget import VideoPlayerWidget


class WebForm(object):
  def __init__(self):
      self.playerWindow = None

  def setupUi(self, Form):
    Form.setObjectName("Form")
    Form.resize(1019, 793)
    self.server = Server()
    self.serverThread = Thread(target=self.server.run, daemon=True)
    self.serverThread.start()

    self.mainLayout = QtWidgets.QVBoxLayout()

    self.player = VideoPlayerWidget(self.server)
    self.webView = QtWebEngineWidgets.QWebEngineView(parent=Form)

    # Создаем кнопку для открытия видеоплеера в отдельном окне
    self.openPlayerButton = QPushButton("Открыть видеоплеер")
    self.openPlayerButton.clicked.connect(self.openPlayerWindow)

    # Добавляем элементы в layout
    self.mainLayout.addWidget(self.openPlayerButton)
    self.mainLayout.addWidget(self.player,stretch=2)
    self.mainLayout.addWidget(self.webView, stretch=3)

    # Устанавливаем layout
    self.setLayout(self.mainLayout)

    #self.webView.setGeometry(QtCore.QRect(0, 30, 1021, 561))
    self.webView.setObjectName("webView")

    self.retranslateUi(Form)
    QtCore.QMetaObject.connectSlotsByName(Form)

  def retranslateUi(self, Form):
    _translate = QtCore.QCoreApplication.translate
    Form.setWindowTitle("Карта")

  # Функция для открытия видеоплеера в отдельном окне
  def openPlayerWindow(self):
    if self.playerWindow == None:
        self.playerWindow = QMainWindow()
        self.playerWindow.setWindowTitle("Видеоплеер")
        self.playerWindow.resize(1000, 440)
        self.playerWindow.setCentralWidget(VideoPlayerWidget(self.server))
        self.playerWindow.show()
    if self.openPlayerButton.text() == "Открыть видеоплеер":
        self.player.mediaPlayer.pause()
        self.openPlayerButton.setText("Закрыть видеоплеер")
    else:
        self.openPlayerButton.setText("Открыть видеоплеер")
    # Скрываем плеер из основного окна
    self.player.setVisible(not self.player.isVisible())
    self.playerWindow.setVisible(not self.player.isVisible())


class ViewTrack(QtWidgets.QWidget, WebForm):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.webView.load(QtCore.QUrl('http://127.0.0.1:3000'))

    def closeEvent(self, e):
        e.ignore()
        self.hide()