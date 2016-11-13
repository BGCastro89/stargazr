import requests
import os

from django.http import JsonResponse
from PIL import Image

def weather(request):
    root_uri = 'https://api.darksky.net'
    key = os.environ.get('DARK_SKY_API_KEY', '')
    action = 'forecast'
    lat = request.GET['lat']
    lng = request.GET['lng']
    lat_lng = ','.join((lat, lng))
    uri = '/'.join((root_uri, action, key, lat_lng))
    response = requests.get(uri)
    data = response.json()
    return JsonResponse(data)

def distance(request):
    root_uri = 'https://maps.googleapis.com'
    key = os.environ.get('GMAPS_API_KEY', '')
    action = 'maps/api/distancematrix/json'
    origins = request.GET['origins']
    destinations = request.GET['destinations']
    units = request.GET['units']
    uri = '/'.join((root_uri, action))
    payload = { 'units': units, 'origins': origins, 'destinations': destinations, 'key': key }
    response = requests.get(uri, params=payload)
    data = response.json()
    return JsonResponse(data)

def brightness(request):
    curr_dir_path = os.path.dirname(os.path.realpath(__file__))
    tiles_dir_path = os.path.join(curr_dir_path, 'tiles')
    lat = float(request.GET['lat'])
    lon = float(request.GET['lng'])

    print "Looking up latitude - %s" % lat
    print "Looking up longitude - %s" % lon
    bin_lat = 0
    bin_lon = 0
    found = False
    # 1024 pixels* (47-11=34) images in lat, 140 deg of coverage
    # Latitudes start at -65.00, end at 74.99
    lat_pixel_res = 140.0/(1024*34)
    long_pixel_res = 360.0/(1024*64)
    # 63 tile longitudinal grids
    for i in xrange(0, 64):
        # 47 tile latitude grids
        for j in xrange(0, 34):
            # Latitudes start at -65.00, end at 74.99
            c_lat = -65.0041666666667 + j * (1024 * lat_pixel_res)
            # Longitudes start at -179.99, end at 179.99
            c_lon = -179.995833333333 + i * (1024 * long_pixel_res)
            min_lat = c_lat - (512 * lat_pixel_res)
            max_lat = c_lat + (512 * lat_pixel_res)
            min_lon = c_lon - (512 * long_pixel_res)
            max_lon = c_lon + (512 * long_pixel_res)

            print "bin lat: %s" % j
            print "bin long: %s" % i
            print "c_lat: %s" % c_lat
            print "c_lon: %s" % c_lon
            print "min_lat: %s" % min_lat
            print "max_lat: %s" % max_lat
            print "min_lon: %s" % min_lon
            print "max_lon: %s" % max_lon
            print ""
            if min_lat <= lat and lat <= max_lat and min_lon <= lon and lon <= max_lon:
                bin_lat = j
                bin_lon = i
                found = True
                break

        if found:
            break

    c_lat = -65.0041666666667 + (j * (1024 * lat_pixel_res))
    c_lon = -179.995833333333 + (i * (1024 * long_pixel_res))
    min_lat = c_lat - (512 * lat_pixel_res)
    max_lat = c_lat + (512 * lat_pixel_res)
    min_lon = c_lon - (512 * long_pixel_res)
    max_lon = c_lon + (512 * long_pixel_res)
    pixel_x = int((lon - min_lon) / lat_pixel_res)
    pixel_y = int((lat - min_lat) / long_pixel_res)

    pixel_x = max(0, min(pixel_x, 1023))
    pixel_y = max(0, min(pixel_y, 1023))

    image_name = "tile_6_%d_%d.png" % (i, j)

    try:
        image_path = os.path.join(tiles_dir_path, image_name)
        print "Trying to open image: %s" % image_path
        image = Image.open(image_path)
        print "Looking up pixel ({},{})".format(pixel_x, pixel_y)
        pixel_value = image.getpixel((pixel_x, pixel_y))
        print image_name, pixel_value
    except IndexError as e:
        print "Error: %s" % e
    except IOError as e:
        print "Error: There's no coverage for %s" % image_name 

    return JsonResponse({'brightness': pixel_value})
