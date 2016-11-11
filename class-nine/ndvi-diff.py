import gc

import numpy as np
import rasterio as rio
from rasterio.mask import mask
from shapely.geometry import Point, MultiPoint, mapping


def min_bounds(paths):
    minb = None
    for path in paths:
        with rio.open('%s/B5.tif' % path, 'r') as src:
            bounds = MultiPoint([
                Point(src.bounds.left, src.bounds.top),
                Point(src.bounds.right, src.bounds.bottom)
            ]).envelope
            if minb is None:
                minb = bounds
            elif minb.area > bounds.area:
                minb = bounds
    return mapping(minb)


def calc_ndvi(path, bounds):
    with rio.open('%s/B5.TIF' % path, 'r') as src:
        meta = src.meta
        cropped, transform = mask(src, [bounds], crop=True)
        nir = cropped
        meta['transform'] = transform

    with rio.open('%s/B4.TIF' % path, 'r') as src:
        cropped, _ = mask(src, [bounds], crop=True)
        r = cropped

    ndvi = (nir - r) / (nir + r)
    del nir
    del r
    gc.collect()

    return (ndvi, meta)

# 36.3698313,36.9390273
# 315108.649429;4026941.82273
# 35.9704593,37.4608783
# 361225.684022;3981766.93195

bounds = min_bounds(['aleppo/2013', 'aleppo/2016'])
bounds = mapping(MultiPoint([
    Point(315108.649429, 4026941.82273),
    Point(361225.684022, 3981766.93195)
]))


first, meta = calc_ndvi('aleppo/2013', bounds)
second, _ = calc_ndvi('aleppo/2016', bounds)

result = second - first

meta['dtype'] = 'float64'
meta['nodata'] = 0
with rio.open('ndvi.tif', 'w', **meta) as dest:
    dest.write(result)
