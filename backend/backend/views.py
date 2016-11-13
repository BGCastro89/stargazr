import requests
import os
import math

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

def gudermannian(x):
    return 2*math.atan(math.exp(x)) - math.pi/2

def inv_gudermannian(y):
    return math.log(math.tan((y + math.pi/2) / 2))

def get_lat_lng_tile(lat, lng, zoom):
    """convert lat/lng to Google-style Mercator tile coordinate (x, y)
    at the given zoom level"""

    lat_rad = lat * math.pi / 180.0
    # "map-centric" latitude, in radians:
    lat_rad = inv_gudermannian(lat_rad)

    x = 2**zoom * (lng + 180.0) / 360.0
    y = 2**zoom * (math.pi - lat_rad) / (2 * math.pi)

    return (x, y)

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

    i, j = get_lat_lng_tile(lat, lon, 6)
    i_pixel_percent = i%1
    j_pixel_percent = j%1
    i = int(i)
    j = int(j)

    pixel_x = i_pixel_percent * 1024
    pixel_y = j_pixel_percent * 1024

    pixel_x = int(max(0, min(pixel_x, 1023)))
    pixel_y = int(max(0, min(pixel_y, 1023)))

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
