import os

import flask
import geojson
import gpxpy
import jinja2
from PyQt5.QtCore import pyqtSignal, QObject
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from geojson import LineString, Feature, FeatureCollection
from engineio.async_drivers import threading
from CoordinateCalculation import CoordinateCalculation
from GPXHandler import GPXHandler
from configs import config
from configs.sign_config import type_signs_with_text, codes_signs

template_dir = os.path.join(os.getcwd(), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

class SignalChangePoint(QObject):
    # создаем свой сигнал
    signal = pyqtSignal()
class Server:
    def __init__(self):
        self.app = Flask(__name__, template_folder='../templates')
        CORS(self.app)
        self.number_point = 0
        self.changePoint = SignalChangePoint()
        self.GPXHandler = GPXHandler()
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
                    arr["id"] = item["properties"]["id"]
                    arr["description"] = item["properties"]["SEM250"] if "SEM250" in item["properties"] else ''
                    new_object.append(arr)
                return new_object

        @self.app.route("/img_type/<image_id>")
        def get_img_type(image_id):
            if 'V' in image_id:
                image_path = rf"./sings/{image_id}"
            else:
                image_path =rf"./sings/V{image_id}.png"

            path_img = os.path.join(os.getcwd(), "sings")
            path_img = os.path.join(path_img, os.path.basename(image_path))

            return flask.send_file(path_img, as_attachment=True)

        @self.app.route("/create_new_line")
        def create_new_line():
            old_line = [float(item) for item in request.args.get('old_line').split(',')]
            new_coordinates =[float(item) for item in request.args.get('new_point').split(',')]
            new_line = CoordinateCalculation.calculate_new_line(old_line, new_coordinates)
            new_line = f'{round(new_line[1],7)},{round(new_line[0],7)}'
            return new_line

        @self.app.route("/save_track")
        def save_track():
            index_offset_track = int(request.args.get('index_offset_track'))
            print(index_offset_track)
            self.GPXHandler.transform_file(index_offset_track)
            return str(index_offset_track)

        @self.app.route("/change_azimuth")
        def change_azimuth():
            second_line = [float(item) for item in request.args.get('line').split(",")]
            lon1, lat1, lon2, lat2 = second_line
            old_direction = CoordinateCalculation.calculate_direction(lon1, lat1, lon2, lat2)[0]

            return str(old_direction)

        @self.app.route("/switch_point")
        def switch_point():
            number_new_point = int(request.args.get('currentNumber'))
            self.number_point = number_new_point
            self.changePoint.signal.emit()

            self.change_dot(number_new_point)
            return str(number_new_point)
        @self.app.route("/all_img")
        def get_all_img():
            img_names = os.listdir('./sings')
            return img_names

        @self.app.route('/save_geojson', methods=['POST'])
        def receive_data():
            new_data = request.get_json()
            features = []
            for item in new_data:
                line = LineString(item["line"])
                # создание объукта описывающего ДЗ
                properties = {"type": item["type"], "azimuth": item["azimuth"], "id": item["id"], "code": int(codes_signs[item["type"]])}
                if item["type"] in type_signs_with_text:
                    properties['MVALUE'] = item["description"]
                    properties['SEM250'] = item["description"]
                features.append(Feature(geometry=line, properties=properties))
            feature_collection = FeatureCollection(features)
            with open(config.PATH_TO_GEOJSON, 'w', encoding='utf-8') as f:
                geojson.dump(feature_collection, f, skipkeys=False, ensure_ascii=False)
            if new_data is None:
                return jsonify({'error': 'No data provided'}), 400
            # Return a success response
            return jsonify({'message': 'Data received successfully'}), 200

    def run(self):
        self.app.run(port=int(os.environ.get("PORT", 3000)))

    def change_dot(self, number):
        self.socketio.emit("change_dot", number)

# Создание экземпляра класса Server
#Server = Server()
#Server.run()
# Запуск сервера
