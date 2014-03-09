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
    city_list = ['Juneau, AK', 'Vancouver, BC', 'Seattle', 'Portland, OR', 'San Francisco, CA', 'Los Angeles, CA']
    city_dict = {}
    for city in city_list:
        lat_c = get_city_loc(city)[0]
        lng_c = get_city_loc(city)[1]
        intensity_list = []
        eq_dict = {}
        for i in range(len(data['earthquakes'])):
        # print(city + ":")
        # for i in range(2):
            stri = str(i + 1)
            timedate = data['earthquakes'][i]['timedate']
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
            intensity_list.append(intensity)
            eq_dict[stri] = [timedate, str(epi_d), str(depth_d), str(mag), str(intensity)]
        intensity_avg = sum(intensity_list) / len(intensity_list)
        city_dict[city] = (str(intensity_avg), eq_dict)
    return city_dict
    # pprint(city_dict)
            # print("Earthquake: " + stri + "\n" +
            #       "Distance: " + str(epi_d) + "\n" +
            #       "Depth distance: " + str(depth_d) + "\n" +
            #       "Magnitude: " + str(mag) + "\n" +
            #       "Intensity: " + str(intensity) + "\n")
            # print("Distance from " + city + ": " + str(epi_d) + "\n" +
            #       "Depth distance from " + city + ": " + str(depth_d) + "\n" +
            #       "Magnitude: " + str(mag) + "\n" +
            #       "Intensity: " + str(intensity) + "\n")


def get_city_loc(city):
    city_list = city.split()
    city_entry = "+".join(city_list)
    url = 'http://maps.google.com/maps/api/geocode/json?address=' + city_entry + '&sensor=false'
    resp = requests.get(url)
    data = json.loads(resp.text)
    lat = data['results'][0]['geometry']['location']['lat']
    lng = data['results'][0]['geometry']['location']['lng']
    return (lat, lng)

if __name__ == '__main__':
    earthquake()
    # if len(sys.argv) > 1 and sys.argv[1] == 'test':
    #     html, encoding = read_search_results()
    # else:

