import gc
import numpy as np
import rasterio as rio
from rasterio.warp import reproject
from rasterio.enums import Resampling


def correct(img):
    mask = np.logical_and(img > 0, img < 65535)
    top = np.percentile(img[mask], 99.9)
    bottom = np.percentile(img[mask], 0.01)
    scaled = (img - bottom) / float(top - bottom) * 65535
    return np.clip(scaled, 0, 65535).astype(np.uint16)

with rio.open('ndvi.tif') as ndvi:
    with rio.open('aleppo/2016/B8.tif') as pan:
        pan_band = pan.read(1)
        newndvi = np.empty(shape=pan_band.shape)
        reproject(ndvi.read(), newndvi,
                  src_transform=ndvi.transform,
                  src_crs=ndvi.crs,
                  dst_transform=pan.transform,
                  dst_crs=pan.crs,
                  resampling=Resampling.bilinear,
                  threads=2)

        pan_scaled = correct(pan_band) / 65536.0
        ndvi_scaled = np.clip(newndvi / np.max(0.60), 0, 1)
        del pan_band
        del newndvi
        gc.collect()
        meta = pan.meta
        meta['photometric'] = 'rgb'
        meta['count'] = 3
        meta['dtype'] = rio.uint8
        meta['nodata'] = 0
        with rio.open('out.tif', 'w', **meta) as out:
            r = 1 - (1 - pan_scaled) * (1 - ndvi_scaled * 221.0 / 255)
            r *= 255
            out.write(r.astype(np.uint8), 1)
            del r
            gc.collect()

            g = 1 - (1 - pan_scaled) * (1 - ndvi_scaled * 207.0 / 255)
            g *= 255
            out.write(g.astype(np.uint8), 2)
            del g
            gc.collect()

            b = 1 - (1 - pan_scaled) * (1 - ndvi_scaled * 14.0 / 255)
            b *= 255
            out.write(b.astype(np.uint8), 3)
            del b
            gc.collect()
