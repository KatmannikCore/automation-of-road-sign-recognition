from threading import Thread

from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets

from Server import Server
from VideoWidget import VideoPlayerWidget


class WebForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1019, 793)

        self.server = Server()
        self.serverThread = Thread(target=self.server.run, daemon=True)
        self.serverThread.start()

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.player = VideoPlayerWidget(self.server)

        self.webView = QtWebEngineWidgets.QWebEngineView(parent=Form)
        self.mainLayout.addWidget(self.player,stretch=2)
        self.mainLayout.addWidget(self.webView, stretch=3)

        self.setLayout(self.mainLayout)
        #self.webView.setGeometry(QtCore.QRect(0, 30, 1021, 561))
        self.webView.setObjectName("webView")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle("ИНСТРУКЦИЯ")
        '''
        with open("///home/dev7/PycharmProjects/po-uvt/index.html", 'r') as f:
            html = f.read()
            self.webView.setHtml(html)
        '''


class ViewTrack(QtWidgets.QWidget, WebForm):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.webView.load(QtCore.QUrl('http://127.0.0.1:3000'))
        #self.webView.load(QtCore.QUrl().fromLocalFile(os.path.split(os.path.abspath(__file__))[0]+r'\web\index.html'))

    def closeEvent(self, e):
        #self.tlaWindow.hide()
        self.player.play()
        e.ignore()
        self.hide()
