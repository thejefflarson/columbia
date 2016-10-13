import fiona
import sys
import pyproj
from shapely.geometry import shape, mapping
from shapely.ops import transform

def project(s_srs, t_srs, x, y, z=None):
    return pyproj.transform(s_srs, t_srs, x, y, z)

with fiona.drivers():
    with fiona.open(sys.argv[1]) as source:
        with fiona.open(sys.argv[2],
                        'w',
                        driver='GeoJSON',
                        crs=source.crs,
                        schema=source.schema) as dest:
            s_srs = pyproj.Proj(**source.crs)
            t_srs = pyproj.Proj(init='epsg:3857')
            for s in source:
                geom = shape(s['geometry'])
                projected = transform(lambda x, y, z=None: pyproj.transform(s_srs, t_srs, x, y, z), geom)
                simplified = projected.simplify(20.0)
                dest.write({
                    'geometry': mapping(simplified),
                    'properties': s['properties']
                })
