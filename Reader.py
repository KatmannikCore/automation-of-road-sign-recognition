import gpxpy.gpx

from configs import config
from Converter import Converter


class Reader:
    def __init__(self, path ):
        gpx_file = open(config.PATH_TO_GPX, 'r')
        self.gpx = gpxpy.parse(gpx_file)
        self.conventer = Converter()

    def get_azimuth(self, indexOfGPS):
        return self.gpx.tracks[0].segments[0].points[indexOfGPS].course


    def get_current_coordinate(self, indexOfGPS):
        latitude = self.gpx.tracks[0].segments[0].points[indexOfGPS].latitude
        longitude = self.gpx.tracks[0].segments[0].points[indexOfGPS].longitude
        return latitude, longitude #self.conventer.coordinateConverter(latitude, longitude, "epsg:4326", "epsg:32635")


    def get_prew_coordinate(self, indexOfGPS):
        latitude = self.gpx.tracks[0].segments[0].points[indexOfGPS - 1].latitude
        longitude = self.gpx.tracks[0].segments[0].points[indexOfGPS - 1].longitude
        return latitude, longitude #self.conventer.coordinateConverter(latitude, longitude, "epsg:4326", "epsg:32635")
    def get_count_dot(self):
        return len(self.gpx.tracks[0].segments[0].points)
    def get_speed(self, indexOfGPS):
        return self.gpx.tracks[0].segments[0].points[indexOfGPS].speed

