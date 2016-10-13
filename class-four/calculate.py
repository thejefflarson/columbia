import fiona


with fiona.drivers():
    with fiona.open('brooklyn-demos.shp') as source:
        props = [s['properties'] for s in source]

# filter out missing data
props = list(filter(lambda x: x.get('black') and x.get('white') and x.get('total_nonh') > 0, props))

# Calculate totals
total = {'black': 0.0, 'white': 0.0, 'total': 0.0}
for prop in props:
    total['black'] += prop['black']
    total['white'] += prop['white']
    total['total'] += prop['total_nonh']

index = 0.0
for prop in props:
    index += abs(prop['black'] / total['black'] - prop['white'] / total['white'])

print(0.5 * index * 100)
