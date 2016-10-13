import fiona
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt


with fiona.drivers():
    with fiona.open('brooklyn-demos.shp') as source:
        props = [s['properties'] for s in source]


# filter out missing data
df = pd.DataFrame.from_records(props)

features = df[['percent_va', 'p_black', 'median_inc']].dropna()

plt.scatter(features['p_black'], features['percent_va'],)
plt.savefig('out.png')

print(features.describe())

model = sm.OLS(features['percent_va'], features[['p_black']])
print(model.fit().summary())

model = sm.OLS(features['percent_va'], features[['p_black', 'median_inc']]).fit()
print(model.summary())

fig = plt.figure(figsize=(12,8))
fig = sm.graphics.plot_regress_exog(model, "p_black", fig=fig)
fig.savefig('p_black.png')

model = sm.OLS(features['percent_va'], features[['median_inc']])
print(model.fit().summary())
