import statsmodels.api as sm
import rasterio as rio
import numpy as np


def correct(img):
    mask = np.logical_and(img > 0, img < 65535)
    top = np.percentile(img[mask], 99.9)
    bottom = np.percentile(img[mask], 0.01)
    scaled = (img - bottom) / (top - bottom) * 65535
    return np.clip(scaled, 0, 65535).astype(np.float64)

X = []
for i in range(1, 8):
    with rio.open('nyc/brooklyn-B%s.TIF' % i) as source:
        band = source.read(1).flatten()
        band = correct(band) / 65535
        X.append(band)

with rio.open('nyc/parks.tif') as parks:
    Y = parks.read(1).flatten().astype(np.float64)

X = np.array(X).transpose()
X = sm.tools.tools.add_constant(X)

model = sm.Logit(Y, X)
res = model.fit()
print(res.summary())

X = []
for i in range(1, 8):
    with rio.open('nyc/manhattan-B%s.tif' % i) as source:
        band = source.read(1)
        shape = band.shape
        band = band.flatten()
        band = correct(band) / 65535
        X.append(band)
        meta = source.meta

X = np.array(X).transpose()
X = sm.tools.tools.add_constant(X)
Y = model.predict(res.params, exog=X)
# convert to probability http://www.ats.ucla.edu/stat/mult_pkg/faq/general/odds_ratio.htm
Y = np.exp(Y) / (1 + np.exp(Y))
meta['count'] = 1
meta['dtype'] = 'float64'
with rio.open('nyc/manhattan-parks.tif', 'w', **meta) as out:
    out.write(Y.reshape(shape), indexes=1)
