from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework.response import Response
import requests
import json

class LocationViewSet(viewsets.ModelViewSet):

def weather(request):
    root_uri = 'https://api.darksky.net'
    api = '0123456789abcdef9876543210fedcba'
    action = 'forecast'
    lat = request.GET['lat']
    lng = request.GET['lng']
    lat_lng = ','.join((lat, lng))
    uri = '/'.join((root_uri, action, api, lat_lng))
    response = requests.get(uri)
    return Response(response.json())