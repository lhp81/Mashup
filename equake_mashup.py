#! /usr/bin/env python

import requests
import json
from pprint import pprint
from math import sin as sin
from math import cos as cos
from math import atan2 as atan2
from math import radians as rad
from math import sqrt as sqrt


def earthquake():
    url = 'http://www.seismi.org/api/eqs/2013?min_magnitude=7'
    resp = requests.get(url)
    data = json.loads(resp.text)
    lat_c = get_city_loc()[0]
    lng_c = get_city_loc()[1]
    # if data['status'] == 'OK':
    # for i in range(len(data['earthquakes'])):
    for i in range(2):
        lat_e = float(data['earthquakes'][i]['lat'])
        lng_e = float(data['earthquakes'][i]['lon'])
        mag = float(data['earthquakes'][i]['magnitude'])
        depth = float(data['earthquakes'][i]['depth'])
        #  Haversine calculation for distance using coordinates.
        R = 6371
        dLat = rad(lat_c - lat_e)
        dLon = rad(lng_c - lng_e)
        lat_er = rad(lat_e)
        lat_cr = rad(lat_c)
        a = sin(dLat/2) * sin(dLat/2) + sin(dLon/2) * sin(dLon/2) * cos(lat_er) * cos(lat_cr)
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        epi_d = R * c
        depth_d = sqrt(depth**2 + epi_d**2)
        intensity = 10000 * mag / depth_d
        # print("Distance from Seattle: " + str(d) + "\n" + "Magnitude: " + str(mag) + "\n")
        print("Distance from Los Angeles: " + str(epi_d) + "\n" +
              "Depth distance from Los Angeles: " + str(depth_d) + "\n" +
              "Magnitude: " + str(mag) + "\n" +
              "Intensity: " + str(intensity) + "\n")
        # print(lat_c, lng_c, lat_e, lng_e, mag, depth)

#         var R = 6371; // km
# var dLat = (lat2-lat1).toRad();
# var dLon = (lon2-lon1).toRad();
# var lat1 = lat1.toRad();
# var lat2 = lat2.toRad();

# var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
#         Math.sin(dLon/2) * Math.sin(dLon/2) * Math.cos(lat1) * Math.cos(lat2);
# var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
# var d = R * c;
    # print(data['count'])
    # print(len(data['earthquakes']))
    # print(len(data))

def get_city_loc():
    # url = 'http://maps.google.com/maps/api/geocode/json?address=seattle&sensor=false'
    url = 'http://maps.google.com/maps/api/geocode/json?address=los+angeles&sensor=false'
    resp = requests.get(url)
    data = json.loads(resp.text)
    lat = data['results'][0]['geometry']['location']['lat']
    lng = data['results'][0]['geometry']['location']['lng']
    return (lat, lng)

earthquake()
