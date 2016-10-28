import random
from statistics import mean


import fiona
from pyproj import Proj, transform as project
from shapely.geometry import Point, shape, mapping
from shapely.ops import transform


def p(geom, s_srs):
    to = Proj(init='EPSG:2831')
    geom['shape'] = transform(lambda x, y, z=None: project(s_srs, to, x, y, z),
                              shape(geom['geometry']))
    return geom

points = []
with fiona.drivers():
    with fiona.open('points.shp') as pts:
        srs = Proj(**pts.crs)
        points = [p(it, srs) for it in pts]

centers = []
for i in range(20):  # get 20 random seeds
    pt = random.choice(points)['shape']
    centers.append(Point(pt.x, pt.y))

# k-means
clusters = [None] * len(points)  # tracking array for cluster assignments
for i in range(20):              # quit after ten iterations
    # assign centers
    for idx, shp in enumerate(points):
        min_dist = float("inf")
        pick = None
        for cidx, center in enumerate(centers):
            dist = shp['shape'].distance(center)
            if dist < min_dist:
                clusters[idx] = cidx
                min_dist = dist

    # calculate new means
    for idx, center in enumerate(centers):
        members = [points[i] for (i, cidx) in enumerate(clusters)
                   if cidx == idx]
        new_x = mean([s['shape'].x for s in members])
        new_y = mean([s['shape'].y for s in members])
        centers[idx] = Point(new_x, new_y)
    print("Iteration %i" % i)

with fiona.drivers():
    with fiona.open('kmeans.json',
                    'w',
                    driver='GeoJSON',
                    crs={'init': 'EPSG:2831'},
                    schema={
                        'geometry': 'Point',
                        'properties': {'cluster': 'int',
                                       'address': 'str'}
                    }) as dest:
        for pidx, cluster in enumerate(clusters):
            dest.write({
                'geometry': mapping(points[pidx]['shape']),
                'properties': {
                    'address': points[pidx]['properties']['address'],
                    'cluster': cluster
                }
            })
