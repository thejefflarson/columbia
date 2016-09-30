import fiona
import sys

with fiona.drivers():
    with fiona.open(sys.argv[1]) as source:
        print(source.crs)
        print(source.driver)
        print(source.schema)
        for shape in source:
            print(shape)
