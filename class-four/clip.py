import fiona
import sys
from shapely.geometry import shape, mapping
from shapely.ops import cascaded_union

with fiona.drivers():
    with fiona.open(sys.argv[1]) as source:
        with fiona.open(sys.argv[2]) as clip:
            dest = fiona.open(sys.argv[3], 'w',
                              driver=source.driver,
                              crs=source.crs,
                              schema=source.schema)
            # convert clip into a list of shapely shapes
            clippers = [shape(s['geometry']) for s in clip]
            for feature in source:
                clipped = []
                geometry = shape(feature['geometry'])
                for clipper in clippers:
                    if clipper.intersects(geometry):
                        clipped.append(clipper.intersection(geometry))

                if clipped:
                    unioned = cascaded_union(clipped)
                    # Sometimes an intersection can return a point
                    # or a linestring
                    if unioned.type == geometry.type:
                        dest.write({
                            'geometry': mapping(unioned),
                            'properties': feature['properties']
                        })
            dest.close()
