import fiona
import sys
from shapely.geometry import shape, mapping
from functools import reduce

with fiona.drivers():
            with fiona.open('class-four/brooklyn-demos.shp') as source:
                for s in source:
                    print(s['properties'])

                
