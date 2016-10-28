import rasterio as rio
import numpy as np

with rio.open('B4.TIF') as red:
    r = red.read(1)
    profile = red.profile

with rio.open('B3.TIF') as green:
    g = green.read(1)

with rio.open('B2.TIF') as blue:
    b = blue.read(1)

profile['count'] = 3
profile['photometric'] = 'RGB'
with rio.open("output.tif", 'w', **profile) as dest:
    dest.write(np.array([r, g, b]), indexes=[1, 2, 3])

nn = 0
for band in [r, g, b]:
    n = np.percentile(band, 99.99)
    if n > nn:
        nn = n

bands = []
for i, band in enumerate([r, g, b]):
    band = np.clip(band, 0, nn)
    bands.append(np.uint16(band / nn * (2 ** 16 - 1)))

with rio.open('output-corrected.tif', 'w', **profile) as dest:
    dest.write(np.array(bands), indexes=[1, 2, 3])
