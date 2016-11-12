import sys
from PIL import Image


if __name__ == "__main__":
    basepath = "astronomy/lp2006/overlay/tiles/"
    lat = float(sys.argv[1])
    lon = float(sys.argv[2])
    bin_lat = 0
    bin_lon = 0
    found = False
    for i in xrange(0, 30):
        for j in xrange(0, 30):
            c_lat = -179.99 + j * (1024 * 0.0083)
            c_lon = -65.0 + i * (1024 * 0.0083)
            min_lat = c_lat - (512 * 0.0083)
            max_lat = c_lat + (512 * 0.0083)
            min_lon = c_lon - (512 * 0.0083)
            max_lon = c_lon + (512 * 0.0083)
            if min_lat <= lat and lat <= max_lat and min_lon <= lon and lon <= max_lon:
                bin_lat = j
                bin_lon = i
                found = True
                break

        if found:
            break

    c_lat = -179.99 + j * (1024 * 0.0083)
    c_lon = -65.0 + i * (1024 * 0.0083)
    min_lat = c_lat - (512 * 0.0083)
    max_lat = c_lat + (512 * 0.0083)
    min_lon = c_lon - (512 * 0.0083)
    max_lon = c_lon + (512 * 0.0083)
    pixel_x = int((lon - min_lon) / 0.0083)
    pixel_y = int((lat - min_lat) / 0.0083)
    image_name = "tile_6_%d_%d.png" % (i, j)
    try:
        image = Image.open(basepath + image_name)
        pixel_value = image.getpixel((pixel_x, pixel_y))
        print image_name, pixel_value
    except:
        print "Error: Coordinates not covered.", image_name
