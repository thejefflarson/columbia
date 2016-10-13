import fiona
import sys
from shapely.geometry import shape, mapping
from functools import reduce

with fiona.drivers():
    with fiona.open('no_border.shp') as source:
        print(shape(s['geometry']))
