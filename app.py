from unicodedata import name
from flask import Flask, render_template, request, jsonify

import json
import pymysql.cursors
import requests
import urllib.request

app = Flask(__name__)

"""
@app.route('/')
def weather():
    response = requests.get("https://api.weather.gov/gridpoints/LOT/75,72/forecast")
    temp = response.json()['properties']['periods'][0]['temperature']
    s = str(temp)
    return s
"""


@app.route('/favorite-cities')
def favcities():
    citylist = []
    connection = pymysql.connect(host='db-mysql-sfo3-58736-do-user-11604989-0.b.db.ondigitalocean.com',
                                 user='doadmin',
                                 password='AVNS_ExpNP5wFgHnMVqd',
                                 database='todoapp',
                                 port=25060,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM weathertable"
            cursor.execute(sql)
            result = cursor.fetchall()
            for i in range(len(result)):
                citylist.append(result[i]['city'])
    print(citylist)
    temp_data = {}
    for c in citylist:
        temp_get = index2(c)['temp']
        temp_data[c] = temp_get
    print(temp_data)
    favList = []
    for city in temp_data:
        temp = temp_data[city]
        print(city, temp)
        obj = {"city": city, "temp": temp}
        favList.append(obj)

    response1 = jsonify(favList)

    return response1


@app.route('/<name>')
def index(name):
    fail_data = {'temp': "N/A", 'forecast': 'N/A'}
    name1 = name.split();
    name_url = '+'.join(name1)
    url = "https://open.mapquestapi.com/geocoding/v1/address?key=A9AWLA8Gm8L5c5KtZ5IT82dhGlO2iZAw&location=" + name_url
    try:
        cds1 = requests.get(url)
    except Exception as e:
        return jsonify(fail_data), 400

    lat1 = cds1.json()["results"][0]["locations"][0]["latLng"]["lat"]
    long1 = cds1.json()["results"][0]["locations"][0]["latLng"]["lng"]

    # Check if data is the default fail output lat/lng
    if lat1 == 39.78373 and long1 == -100.445882:
        return fail_data

    gridpts = requests.get("https://api.weather.gov/points/" + str(lat1) + "," + str(long1))
    gp_response1 = gridpts.json()["properties"]["forecast"]
    response1 = requests.get(gp_response1)
    print_temp = str(response1.json()['properties']['periods'][0]['temperature'])

    temp1 = response1.json()['properties']['periods'][0]['temperature']
    s_temp1 = str(temp1)

    forecast1 = response1.json()['properties']['periods'][0]['detailedForecast']

    data = {'temp': s_temp1, 'forecast': forecast1}
    return jsonify(data), 200


def index2(name):
    fail_data = {'temp': "N/A", 'forecast': 'N/A'}
    name1 = name.split();
    name_url = '+'.join(name1)
    url = "https://open.mapquestapi.com/geocoding/v1/address?key=A9AWLA8Gm8L5c5KtZ5IT82dhGlO2iZAw&location=" + name_url
    print(url)
    try:
        cds1 = requests.get(url)
    except Exception as e:
        return fail_data

    lat1 = cds1.json()["results"][0]["locations"][0]["latLng"]["lat"]
    long1 = cds1.json()["results"][0]["locations"][0]["latLng"]["lng"]

    # Check if data is the default fail output lat/lng
    if lat1 == 39.78373 and long1 == -100.445882:
        return fail_data

    gridpts = requests.get("https://api.weather.gov/points/" + str(lat1) + "," + str(long1))
    gp_response1 = gridpts.json()["properties"]["forecast"]
    response1 = requests.get(gp_response1)

    temp1 = response1.json()['properties']['periods'][0]['temperature']
    s_temp1 = str(temp1)

    forecast1 = response1.json()['properties']['periods'][0]['detailedForecast']

    data = {'temp': s_temp1, 'forecast': forecast1}
    return data
