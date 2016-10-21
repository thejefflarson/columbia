from math import atan, sinh, pi as π

import fiona
from flask import Flask
import json
from shapely.geometry import MultiPoint, Point, mapping, shape
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# from https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
def tile2ll(x, y, z):
    n = 2 ** z
    lon = x / n * 360.0 - 180.0
    lat = atan(sinh(π * (1 - 2 * y / n))) * 180.0 / π
    return [lon, lat]


@app.route("/<x>/<y>/<z>.json")
def tile(x=None, y=None, z=None):
    if not (x and y and z):
        raise Exception('Need x, y, and z got: %s, %s, %s' % (x, y, z))
    with fiona.drivers():
        with fiona.open('world.shp') as source:
            x, y, z = [float(x), float(y), float(z)]
            minx, miny = tile2ll(x, y, z)
            maxx, maxy = tile2ll(x + 1, y + 1, z)
            bbox = MultiPoint([
                Point(minx, miny),
                Point(minx, maxy),
                Point(maxx, maxy),
                Point(maxx, miny)
            ]).envelope
            print(minx, miny, maxx, maxy)
            features = []
            for _, s in source.items(bbox=(minx, miny, maxx, maxy)):
                geom = shape(s['geometry'])
                if geom.intersects(bbox):
                    intsx = geom.intersection(bbox)
                    features.append({
                        'geometry': mapping(intsx),
                        'properties': s['properties'],
                        'type': 'Feature'
                    })

            return json.dumps({'land':{
                'type': 'FeatureCollection',
                'features': features
            }})

if __name__ == "__main__":
    app.run()
