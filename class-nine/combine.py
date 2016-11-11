import numpy as np
import rasterio as rio
from rasterio.warp import reproject
from rasterio.enums import Resampling

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
