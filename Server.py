
import os

import geojson
import gpxpy
import jinja2
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO

from CoordinateCalculation import CoordinateCalculation
from configs import config

template_dir = os.path.join(os.getcwd(), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class Server:
    def __init__(self):
        self.app = Flask(__name__, template_folder='../templates')
        CORS(self.app)
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
        @self.app.route("/geojson")
        def get_geojson():
            with open(config.PATH_TO_GEOJSON, encoding='utf-8') as f:
                data = geojson.load(f)["features"]
                new_object = []
                for item in data:
                    arr = {}
                    arr["coordinates"] = item["geometry"]["coordinates"]
                    arr["azimuth"] = float(item["properties"]["azimuth"])
                    arr["type"] = item["properties"]["type"]
                    new_object.append(arr)
                return new_object
        @self.app.route("/img_type/<image_id>")
        def get_img_type(image_id):
            image_path =rf"./sings/V{image_id}.png"
            return send_from_directory(os.path.dirname(image_path), os.path.basename(image_path), as_attachment=True)
        @self.app.route("/create_new_line")
        def create_new_line():
            old_line = [float(item) for item in request.args.get('old_line').split(',')]
            new_coordinates =[float(item) for item in request.args.get('new_point').split(',')]
            new_line = CoordinateCalculation.calculate_new_line(old_line, new_coordinates)
            new_line = f'{round(new_line[1],7)},{round(new_line[0],7)}'
            return new_line
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
