#! /bin/bash

ogr2ogr brooklyn.shp tl_2016_us_county.shp -sql "select * from tl_2016_us_county where COUNTYFP = '047' and STATEFP = '36'" -t_srs 'EPSG:32618'

ogr2ogr manhattan.shp tl_2016_us_county.shp -sql "select * from tl_2016_us_county where COUNTYFP = '061' and STATEFP = '36'" -t_srs 'EPSG:32618'

ogr2ogr parks.json tl_2016_36_arealm.shp -f GeoJSON -sql "select * from tl_2016_36_arealm where MTFCC like 'K218%'" -t_srs 'EPSG:32618'

# from https://github.com/dwtkns/gdal-cheat-sheet
function ogr_extent() {
    if [ -z "$1" ]; then
        echo "Missing arguments. Syntax:"
        echo "  ogr_extent <input_vector>"
        return
    fi
    EXTENT=$(ogrinfo -al -so $1 |\
        grep Extent |\
        sed 's/Extent: //g' |\
        sed 's/(//g' |\
        sed 's/)//g' |\
        sed 's/ - /, /g')
    EXTENT=`echo $EXTENT | awk -F ',' '{print $1 " " $4 " " $3 " " $2}'`
    echo -n "$EXTENT"
}

for i in $( ls *.TIF ); do
    gdal_translate $i brooklyn-$i -projwin $(ogr_extent brooklyn.shp)
    gdal_translate $i manhattan-$i -projwin $(ogr_extent manhattan.shp)
done

rio rasterize parks.tif --like brooklyn-B1.TIF < parks.json
