from pyproj import Proj, transform
from pyproj import Transformer

class Converter():
    def __init__(self):
        pass

    def coordinateConverter(self, lat, lon, epsg1, epsg2):
        transformer = Transformer.from_crs(epsg1, epsg2)
        sm = transformer.transform(lat, lon)
        return sm
