import fiona
import sys
from shapely.ops import unary_union
from shapely.geometry import shape, mapping
from functools import reduce

with fiona.drivers():
    with fiona.open(sys.argv[1]) as source:
        with fiona.open(sys.argv[2],
                        'w',
                        driver=source.driver,
                        crs=source.crs,
                        schema={'geometry': 'Polygon',
                                'properties': []}) as dest:
            polys = [shape(s['geometry']) for s in source]
            dest.write({
                'geometry': mapping(reduce(lambda x, y: x.union(y), polys)),
                'properties':{}
            })
