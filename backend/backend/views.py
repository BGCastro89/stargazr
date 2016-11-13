from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

import requests
import json
import os

renderer_classes = (JSONRenderer, )

def weather(request):
    root_uri = 'https://api.darksky.net'
    api = os.environ.get('DARK_SKY_API_KEY', '')
    action = 'forecast'
    lat = request.GET['lat']
    lng = request.GET['lng']
    lat_lng = ','.join((lat, lng))
    uri = '/'.join((root_uri, action, api, lat_lng))
    response = requests.get(uri)
    data=response.json()
    return Response(data)