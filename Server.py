import os

import gpxpy
from flask import Flask, render_template, request
from flask_cors import CORS
from flask_socketio import SocketIO
from engineio.async_drivers import threading
from configs import config

import jinja2

template_dir = os.path.join(os.getcwd(),"templates")
with open("data.txt", "w") as file:
    file.write(f"{template_dir}")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

config.VIDEOS = os.listdir(r'D:\Urban\vid\test\GOPR0064')


class Server:
    def __init__(self):
        self.app = Flask(__name__, template_folder='../templates')
        CORS(self.app)
        self.dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), rf"D:\Urban\vid\test\GOPR0064")
        self.socketio = SocketIO()
        self.socketio.init_app(self.app, cors_allowed_origins="*", async_mode="threading")

        @self.app.route('/')
        def index():
            template = jinja_env.get_template('index.html')
            return template.render()

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
