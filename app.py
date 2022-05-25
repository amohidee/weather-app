from unicodedata import name
from flask import Flask, render_template, request, jsonify

import datetime
import json
import pymysql.cursors
import requests
import urllib.request

app = Flask(__name__)

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

        for i in range(len(result)):
            city = result[i]['city']
            response = requests.get("https://oyster-app-rh2np.ondigitalocean.app/" + city)
            temp = response.json()["temp"]
            forecast = response.json()["forecast"]
            print(forecast)
            sql = "UPDATE weathertable SET temp = %s, forecast = %s WHERE city = %s"
            cursor.execute(sql, (temp, forecast, city))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

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
    print(citylist)
    temp_data = {}
    for c in citylist:
        temp_get = index2(c)['temp']
        print("temp_get: ")
        print(temp_get)
        temp_data[c] = temp_get
    print(temp_data)
    response1 = jsonify(temp_data)
    return response1


@app.route('/<name>')
def index(name):
    fail_data = {'temp': "N/A", 'forecast': 'N/A'}
    url = "https://open.mapquestapi.com/geocoding/v1/address?key=A9AWLA8Gm8L5c5KtZ5IT82dhGlO2iZAw&location=" + name
    try:
        cds1 = requests.get(url)
    except Exception as e:
        return jsonify(fail_data), 400
    if cds1.json()["results"][0]["locations"][0]["adminArea5"] == "":
        return jsonify(fail_data), 400
    lat1 = cds1.json()["results"][0]["locations"][0]["latLng"]["lat"]
    long1 = cds1.json()["results"][0]["locations"][0]["latLng"]["lng"]

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

    url = "https://open.mapquestapi.com/geocoding/v1/address?key=A9AWLA8Gm8L5c5KtZ5IT82dhGlO2iZAw&location=" + name
    try:
        cds1 = requests.get(url)
    except Exception as e:
        return jsonify(fail_data), 400
    if cds1.json()["results"][0]["locations"][0]["adminArea5"] == "":
        return jsonify(fail_data), 400
    lat1 = cds1.json()["results"][0]["locations"][0]["latLng"]["lat"]
    long1 = cds1.json()["results"][0]["locations"][0]["latLng"]["lng"]

    gridpts = requests.get("https://api.weather.gov/points/" + str(lat1) + "," + str(long1))
    print(gridpts.json()["properties"]["forecast"])
    gp_response1 = gridpts.json()["properties"]["forecast"]
    response1 = requests.get(gp_response1)
    print_temp = str(response1.json()['properties']['periods'][0]['temperature'])
    print("TEMPERATURE: " + print_temp)

    temp1 = response1.json()['properties']['periods'][0]['temperature']
    s_temp1 = str(temp1)

    forecast1 = response1.json()['properties']['periods'][0]['detailedForecast']

    data = {'temp': s_temp1, 'forecast': forecast1}
    return data