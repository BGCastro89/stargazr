from django.http import JsonResponse
import requests
import os

def weather(request):
    root_uri = 'https://api.darksky.net'
    api = os.environ.get('DARK_SKY_API_KEY', '')
    action = 'forecast'
    lat = request.GET['lat']
    lng = request.GET['lng']
    lat_lng = ','.join((lat, lng))
    uri = '/'.join((root_uri, action, api, lat_lng))
    response = requests.get(uri)
    data = response.json()
    return JsonResponse(data)