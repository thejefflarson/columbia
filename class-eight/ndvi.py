import sys

import numpy as np
import rasterio as rio

bands = []
for i in [5, 4]:
    with rio.open('nyc/B%s.TIF' % i) as raster:
        bands.append(raster.read(1))
        profile = raster.meta

nir, r = bands
ndvi = (nir - r) / float(nir + r) + 1


def correct(img):
    mask = np.logical_and(img > 0, img < 65535)
    top = np.percentile(img[mask], 99.9)
    bottom = np.percentile(img[mask], 0.01)
    scaled = (img - bottom) / float(top - bottom) * 65535
    return np.clip(scaled, 0, 65535).astype(np.uint16)

img = correct(np.array(ndvi))
profile['count'] = img.shape[0]
profile['photometric'] = 'RGB'
with rio.open('nyc/ndvi.tif', 'w', **profile) as dest:
    dest.write(correct(img), indexes=list(range(img.shape[0] + 1))[1:])
