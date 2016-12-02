import rasterio as rio
import numpy as np
import math
from scipy.ndimage import generic_filter

with rio.open("durango.tif") as source:
    meta = source.meta
    dem = source.read(1)


def normalize(x, y, z):
    s = math.sqrt(x*x + y*y + z*z)
    return [x / s, y / s, z / s]


# from http://sunandblackcat.com/tipFullView.php?l=eng&topicid=6
def shade(args):
    args = args.reshape(3, 3)
    dx = args[1][0] - args[1][2]
    dy = args[0][1] - args[2][1]
    vec = normalize(dx, dy, 0.5)
    light = normalize(-0.7, -0.7, 0.3)
    return np.array(vec).dot(np.array(light))

dem = (dem - np.min(dem)) / (np.max(dem) - np.min(dem))
shaded = generic_filter(dem, shade, size=(3, 3))
shaded = (shaded - np.min(shaded)) / (np.max(shaded) - np.min(shaded))
shaded *= 255
print(np.min(shaded), np.max(shaded))

meta['dtype'] = 'uint8'
meta['nodata'] = 0
with rio.open('shaded.tif', 'w', **meta) as dest:
    dest.write(shaded.reshape(dem.shape).astype(np.uint8), indexes=1)
