import fiona
import sys

with fiona.drivers():
    with fiona.open(sys.argv[1]) as source:
        with fiona.open(sys.argv[2],
                        'w',
                        driver=source.driver,
                        crs=source.crs,
                        schema=source.schema) as dest:
            dest.writerecords(source)
