import math
import numpy as np
import rasterio as rio


with rio.open('nyc.tif') as raster:
    img = raster.read()
    profile = raster.meta


def c(img):
    nn = np.percentile(img[img > 0], 99.99)
    s = img.astype(np.float64) / nn
    #return s.astype(np.uint16)
    levels, bins = np.histogram(s[img > 0].flat, bins=2**16)
    cdf = levels.cumsum()
    print(cdf[-1])
    cdf = cdf / float(cdf[-1])
    bins = (bins[:1] + bins[:-1]) / 2.0
    corrected = np.interp(img.flat, bins, cdf).reshape(img.shape)
    corrected[img == 0] = 0
    corrected *= 65535
    corrected = np.floor(corrected).astype(np.uint16)
    print(corrected.min(), corrected.max(),
          corrected.mean(), corrected.std())
    return corrected


profile['photometric'] = 'RGB'
with rio.open('output-corrected.tif', 'w', **profile) as dest:
    dest.write(c(img), indexes=[1,2,3])

# color utilities
# convert to xyz
