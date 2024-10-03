import geojson
from geojson import Feature, FeatureCollection

geometry_plate = {"type": "LineString", "coordinates": [[27.2, 54.2], [27.2, 54.2]]}
features = [Feature(geometry=geometry_plate, properties={"name": 'пінкавічы'})]
feature_collection = FeatureCollection(features)
with open(rf'1.geojson', 'w', encoding="utf-8") as f:
  geojson.dump(feature_collection, f,skipkeys=False, ensure_ascii=False)

#'аснежыцы'
#'пінкавічы'