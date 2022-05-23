from unicodedata import name
from flask import Flask, render_template, request, jsonify

import datetime
import json
import requests
import urllib.request
from geocodio import GeocodioClient

app = Flask(__name__)

client = GeocodioClient("8186a8b0b162662bc0c06ca6cab28a88b6b661b")

"""
@app.route('/')
def weather():
    response = requests.get("https://api.weather.gov/gridpoints/LOT/75,72/forecast")
    temp = response.json()['properties']['periods'][0]['temperature']
    s = str(temp)
    return s
"""

@app.route('/<name>')
def index(name):

    fail_data = {'temp': "N/A"}

    try: 
        coords1 = client.geocode(name)
    except Exception as e:
        return jsonify(fail_data), 400
    lat1 = coords1["results"][0]["location"]["lat"]
    long1 = coords1["results"][0]["location"]["lng"]
    print(name)
    print(lat1)
    print(long1)

    gridpts = requests.get("https://api.weather.gov/points/" + str(lat1) + "," + str(long1))
    print(gridpts.json()["properties"]["forecast"])
    gp_response1 = gridpts.json()["properties"]["forecast"]
    response1 = requests.get(gp_response1)
    print("TEMPERATURE")
    print(response1.json()['properties']['periods'][0]['temperature'])
    temp1 = response1.json()['properties']['periods'][0]['temperature']
    s_temp1 = str(temp1)

    address = client.reverse((lat1, long1))
    print(address["results"][0]["address_components"]["city"])
    address_city = address["results"][0]["address_components"]["city"]

    data = {'temp': s_temp1}
    return jsonify(data), 200
