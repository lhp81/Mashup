#! /usr/bin/env python

import json
from pprint import pprint
import re
import requests
from math import sin as sin
from math import cos as cos
from math import atan2 as atan2
from math import radians as rad
from math import sqrt as sqrt


def resolve_path(path):
    urls = [(r'^$', cities),
            (r'^cities/(.+)$', city)]
    matchpath = path.lstrip('/')
    for regexp, func in urls:
        match = re.match(regexp, matchpath)
        if match is None:
            continue
        args = match.groups([])
        return func, args
    raise NameError


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


def get_city_loc(city):
    city_list = city.split()
    city_entry = "+".join(city_list)
    url = 'http://maps.google.com/maps/api/geocode/json?address=' + city_entry + '&sensor=false'
    resp = requests.get(url)
    data = json.loads(resp.text)
    lat = data['results'][0]['geometry']['location']['lat']
    lng = data['results'][0]['geometry']['location']['lng']
    return (lat, lng)

eq_dict = earthquake()


def cities():
    all_cities = [key for key in eq_dict]
    mean_intensity = [eq_dict[city][0] for city in all_cities]
    body = ['<h1>West Coast City Earthquake Data for 2013</h1>', '<ul>']
    item_template = ('<li><strong><a href="/cities/{0}">{0}</a></strong>'
                     ' (Mean Intensity: {1})</li>')
    for city in all_cities:
        mintensity = mean_intensity[all_cities.index(city)]
        body.append(item_template.format(city, mintensity))
    body.append('</ul>')
    return '\n'.join(body)


def city(city):
    pre_body = '<h1>{0} Data:</h1>'
    body = [pre_body.format(city)]
    item_template = ('<table>'
                    '<tr><th>Event time:</th><td>{0} km</td></tr>'
                    '<tr><th>Epicenter distance from {1}:</th><td>{2} km</td></tr>'
                    '<tr><th>Depth Distance from {1}:</th><td>{3} km</td></tr>'
                    '<tr><th>Magnitude:</th><td>{4}</td></tr>'
                    '<tr><th>Intensity:</th><td>{5}</td></tr>'
                    '</table><br />')

    for key in eq_dict[city][1]:
        timedate = eq_dict[city][1][key][0]
        city_distance = eq_dict[city][1][key][1]
        depth_dist = eq_dict[city][1][key][2]
        magnitude = eq_dict[city][1][key][3]
        intensity = eq_dict[city][1][key][4]
        body.append(item_template.format(timedate, city, city_distance,
                    depth_dist, magnitude, intensity))
    body.append('<a href="/">Back to the list</a>')
    return '\n'.join(body)


def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8000, application)
    srv.serve_forever()
