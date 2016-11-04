import sys

import numpy as np
import rasterio as rio

bands = []
for i in [5, 4]:
    with rio.open('brazil/B%s.TIF' % i) as raster:
        bands.append(raster.read(1).astype(np.float32))
        profile = raster.meta

nir, r = bands
ndvi = (nir - r) / (nir + r)

profile['dtype'] = 'float32'
profile['nodata'] = 0
with rio.open('brazil/ndvi.tif', 'w', **profile) as dest:
    dest.write(ndvi, 1)
