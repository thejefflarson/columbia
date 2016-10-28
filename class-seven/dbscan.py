from collections import deque
from operator import itemgetter

import fiona
from pyproj import Proj, transform as project
from shapely.geometry import shape, mapping
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

# tracking array for cluster assignments
clusters = [False] * len(points)
# DBSCAN
neighbors = []

for pt in points:
    nearest = []
    for nidx, o in enumerate(points):
        distance = o['shape'].distance(pt['shape'])
        if distance < 660:
            nearest.append((nidx, distance))
    nearest = sorted(nearest, key=itemgetter(1))
    print(len(nearest))
    neighbors.append(list(map(itemgetter(0), nearest)))

c = 0
for idx, _ in enumerate(points):
    # we only visit each point once
    if clusters[idx] is not False:
        continue

    if len(neighbors[idx]) < 10:
        clusters[idx] = -1
        continue

    c += 1
    clusters[idx] = c
    nearest = deque(neighbors[idx])
    while len(nearest) > 0:
        nidx = nearest.popleft()
        if clusters[nidx] is False:
            nearby = neighbors[nidx]
            if len(nearby) >= 10:
                nearest.extend(nearby)
            clusters[nidx] = c
print(clusters)

with fiona.drivers():
    with fiona.open('knn.json',
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
