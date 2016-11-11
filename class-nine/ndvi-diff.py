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
    ndvi[nir == 0] = 0
    ndvi[r == 0] = 0
    del nir
    del r
    gc.collect()

    return (ndvi, meta)


bounds = min_bounds(['aleppo/2013', 'aleppo/2016'])

first, _ = calc_ndvi('aleppo/2013', bounds)
second, meta = calc_ndvi('aleppo/2016', bounds)
result = second - first
result = (result - np.mean(result) / np.std(result))
result = np.clip(result, 0, 1).reshape(second.shape)
result[first == 0] = 0
result[second == 0] = 0
meta['dtype'] = 'float64'
meta['nodata'] = 0
with rio.open('ndvi.tif', 'w', **meta) as dest:
    dest.write(result)
