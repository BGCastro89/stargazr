from django.http import JsonResponse
import requests
import os

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
