
from flask import Flask, render_template, send_file, request
import os

from flask_socketio import SocketIO, emit

from configs import config
from flask_cors import CORS
import gpxpy

config.VIDEOS = os.listdir(r'D:\Urban\vid\test\GOPR0064')
class Server:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), rf"D:\Urban\vid\test\GOPR0064")
        self.socketio = SocketIO()
        self.socketio.init_app(self.app)

        @self.app.route('/')
        def index():
            return render_template('index.html')


        @self.app.route("/track")
        def get_track():
            result = []
            gpx_file = open(config.PATH_TO_GPX, 'r')
            gpx = gpxpy.parse(gpx_file)
            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        result.append([point.latitude, point.longitude])
            return result

    def run(self):
        self.app.run(port=int(os.environ.get("PORT", 3000)))

    def shutdown_server(self):

        print("Остановка сервера...")
        # Вызываем сигнал остановки
        func = request.environ.get('werkzeug.server.shutdown')
        if func is not None:
            func()

    def change_dot(self, number):
        self.socketio.emit("change_dot", number)


# Создание экземпляра класса Server
#Server = Server()
#Server.run()
# Запуск сервера