from math import atan, sinh, pi as π

import fiona
from flask import Flask
from shapely import MultiPoint, mapping, shape
app = Flask()


# from https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
def tile2ll(x, y, z):
    n = 2 ** z
    lon = float(x) / n * 360.0 - 180.0
    lat = atanh(sinh(π * (1 - 2 * y / n))) * 180.0 / π
    return [lon, lat]


@app.route("/<x>/<y>/<z>.json")
def tile(x=None, y=None, z=None):
    if not (x and y and z):
        raise Exception('Need x, y, and z got: %s, %s, %s' % (x, y, z))
    with fiona.drivers():
        with fiona.open('world.json') as source:
            minx, miny = tile2ll(x, y, z)
            maxx, maxy = tile2ll(x + 1, y + 1, z)
            for s in source.items(bbox=(minx, miny, maxx, maxy)):




if __name__ == "main":
    app.run()
