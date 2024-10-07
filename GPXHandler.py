import gpxpy.gpx

from configs import config
from Converter import Converter
import xml.etree.ElementTree as ET

class GPXHandler:
    def __init__(self):
        self.gpx_file = open(config.PATH_TO_GPX, 'r')
        self.gpx = gpxpy.parse(self.gpx_file)
        self.conventer = Converter()
        ET.register_namespace("", "https://www.gpsbabel.org")
        ET.register_namespace("", "http://www.topografix.com/GPX/1/0")

    def get_azimuth(self, indexOfGPS):
        return self.gpx.tracks[0].segments[0].points[indexOfGPS].course

    def get_current_coordinate(self, indexOfGPS):
        latitude = self.gpx.tracks[0].segments[0].points[indexOfGPS].latitude
        longitude = self.gpx.tracks[0].segments[0].points[indexOfGPS].longitude
        return latitude, longitude  #self.conventer.coordinateConverter(latitude, longitude, "epsg:4326", "epsg:32635")

    def get_prew_coordinate(self, indexOfGPS):
        latitude = self.gpx.tracks[0].segments[0].points[indexOfGPS - 1].latitude
        longitude = self.gpx.tracks[0].segments[0].points[indexOfGPS - 1].longitude
        return latitude, longitude  #self.conventer.coordinateConverter(latitude, longitude, "epsg:4326", "epsg:32635")

    def get_count_dot(self):
        return len(self.gpx.tracks[0].segments[0].points)

    def get_speed(self, indexOfGPS):
        return self.gpx.tracks[0].segments[0].points[indexOfGPS].speed

    def transform_file(self, number_offset):
        tree = ET.parse(config.PATH_TO_GPX)
        root = tree.getroot()
        if number_offset > 0:
            self.add_point(number_offset, root)
        else:
            for index in range(abs(number_offset)):
                self.remove_first_point(abs(number_offset), root)
        tree.write(config.PATH_TO_GPX, encoding='utf-8', xml_declaration=True)

    def remove_first_point(self, cound_delete_points, root):
            trkpt = root[2][0][0]
            if trkpt is not None:
                root[2][0].remove(trkpt)
            return root

    def add_point(self, count_points, root):
        coordinates = root[2][0][0].attrib
        properties = root[2][0][0]
        trkpt = self.create_new_trkpt(coordinates, properties)
        for index in range(count_points):
            root[2][0].insert(0, trkpt)
        return root

    def create_new_trkpt(self, coordinates, properties):
        trkpt = ET.Element('trkpt', lat=str(coordinates["lat"]), lon=str(coordinates['lon']))
        ET.SubElement(trkpt, 'ele').text = str(properties[0].text)
        ET.SubElement(trkpt, 'time').text = properties[1].text
        ET.SubElement(trkpt, 'course').text = str(properties[2].text)
        ET.SubElement(trkpt, 'speed').text = str(properties[3].text)
        ET.SubElement(trkpt, 'geoidheight').text = str(properties[4].text)
        ET.SubElement(trkpt, 'fix').text = properties[5].text
        ET.SubElement(trkpt, 'sat').text = str(properties[6].text)
        ET.SubElement(trkpt, 'hdop').text = str(properties[7].text)
        ET.SubElement(trkpt, 'vdop').text = str(properties[8].text)
        ET.SubElement(trkpt, 'pdop').text = str(properties[9].text)
        return trkpt


