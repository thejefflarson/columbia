import csv
import fiona
import requests
import sys
import time

KEY = "mapzen-R2zbE4V"
with fiona.drivers():
    with fiona.open('points.shp',
                    'w',
                    crs='EPSG:4326',
                    driver='ESRI Shapefile',
                    schema={
                        'geometry': 'Point',
                        'properties': {'address': 'str'}
                    }) as dest:
        with open('addresses.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    int(row['number'])
                except ValueError:
                    next

                addy = ' '.join([row['number'], row['name'], "New York", "NY", row['zip']])
                resp = requests.get("https://search.mapzen.com/v1/search?text=%s&api_key=%s" % (addy, KEY))
                json = resp.json()
                sys.stdout.write('.')
                sys.stdout.flush()
                if ('features' in json
                    and json['features'][0]
                    and json['features'][0]['properties']['confidence'] == 1):
                    dest.write({
                        'geometry': json['features'][0]['geometry'],
                        'properties': {'address': addy}
                    })
                    time.sleep(1/10.0)
                else:
                    print(json)
