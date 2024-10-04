require([
    "esri/Map",
    "esri/views/MapView",
    "esri/layers/VectorTileLayer",
    "esri/layers/GraphicsLayer",
    "esri/Graphic",
    "esri/geometry/Polyline",
    "esri/geometry/Point",
    "esri/symbols/SimpleLineSymbol",
    "esri/symbols/PictureMarkerSymbol",
    "esri/identity/IdentityManager",
  ], function (
    Map,
    MapView,
    VectorTileLayer,
    GraphicsLayer,
    Graphic,
    Polyline,
    Point,
    SimpleLineSymbol,
    PictureMarkerSymbol,
    IdentityManager
  ) {
    var map = new Map();
    IdentityManager.registerToken({
      server: "https://gis.maps.by/arcgis",
      token: "arcgis",
    });

    var view = new MapView({
      container: "viewDiv",
      map: map,
      constraints: {
        minZoom: 6,
        maxZoom: 23,
        rotationEnabled: false,
      },
      center: [27.561524, 53.902496],
      zoom: 13,
    });

    var layer = new VectorTileLayer({
      url: "https://gis.maps.by/arcgis/rest/services/Hosted/VectorTile_240522/VectorTileServer",
    });

    map.add(layer);

    var graphicsLayer = new GraphicsLayer();
    map.add(graphicsLayer);

    const displayZoomLevel = 15; 

    function loadGeoJSON() {
      fetch("./city.geojson")
        .then((response) => response.json())
        .then((data) => {
          processGeoJSON(data);
        })
        .catch((error) =>
          console.error("Ошибка при загрузке GeoJSON:", error)
        );
    }

    function getImageUrl(type) {
      const match = type.match(/[0-9.]+/);
      const fileName = match ? match[0] : "";
      return `./100/V${fileName}.png`;
    }

    function processGeoJSON(geojson) {
      geojson.features.forEach((feature) => {
        const coordinates = feature.geometry.coordinates;
        const properties = feature.properties;
        const azimuth = properties.azimuth;
        const imageType = properties.type;

        const lineStart = {
          x: coordinates[0][0],
          y: coordinates[0][1],
        };
        const lineEnd = {
          x: coordinates[1][0],
          y: coordinates[1][1],
        };

        const polyline = new Polyline({
          paths: [
            [
              [lineStart.x, lineStart.y],
              [lineEnd.x, lineEnd.y],
            ],
          ],
        });

        const lineGraphic = new Graphic({
          geometry: polyline,
          symbol: {
            type: "simple-line",
            color: "red",
            width: 2,
          },
        });
        graphicsLayer.add(lineGraphic);

        const imageUrl = getImageUrl(imageType);
        const image = new Image();
        image.src = imageUrl;
        image.onload = function () {
          const scaleFactor = 0.50;
          const pictureMarkerSymbol = new PictureMarkerSymbol({
            url: imageUrl,
            width: image.width * scaleFactor,
            height: image.height * scaleFactor,
            angle: azimuth,
          });

          const imageCenterPoint = new Point({
            x: (lineStart.x + lineEnd.x) / 2,
            y: (lineStart.y + lineEnd.y) / 2,
          });

          const imageGraphic = new Graphic({
            geometry: imageCenterPoint,
            symbol: pictureMarkerSymbol,
          });

          imageGraphic._imageUrl = imageUrl;

          graphicsLayer.add(imageGraphic);
        };
      });
    }

    function updateVisibleGraphics() {
      const currentZoom = view.zoom; 
      const visibleExtent = view.extent;

      graphicsLayer.graphics.forEach((graphic) => {
        const point = graphic.geometry;
        if (visibleExtent.contains(point)) {
          if (currentZoom >= displayZoomLevel) {
            graphic.visible = true;
          } else {
            graphic.visible = false;
          }
        } else {
          graphic.visible = false;
        }
      });
    }

    view.watch("stationary", function () {
      updateVisibleGraphics();
    });

    view.watch("zoom", function () {
      updateVisibleGraphics();
    });

    loadGeoJSON();
  });