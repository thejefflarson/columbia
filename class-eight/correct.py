import numpy as np
import rasterio as rio

with rio.open('nyc.tif') as raster:
    img = raster.read()
    profile = raster.meta


def correct(img):
    mask = np.logical_and(img > 0, img < 65535)
    top = np.percentile(img[mask], 99.9)
    bottom = np.percentile(img[mask], 0.01)
    scaled = (img - bottom) / float(top - bottom) * 65535
    return np.clip(scaled, 0, 65535).astype(np.uint16)

profile['photometric'] = 'RGB'
with rio.open('output-corrected.tif', 'w', **profile) as dest:
    dest.write(correct(img), indexes=[1, 2, 3])
