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
            (r'^^/cities/(id[\d]+)$', city)]
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
city_dict = [dict(id=city, title=database[id]['title']) for id in
                  temp_dict]


def cities():
    all_cities = [key for key in temp_dict]
    mean_intensity = [temp_dict[city][0] for city in all_cities]
    body = ['<h1>West Coast City Earthquake Data</h1>', '<ul>']
    item_template = ('<li><strong><a href="/cities/{0}">{0}</a></strong>'
                     '(Mean Intensity: {1})</li>')
    for city in all_cities:
        mintensity = mean_intensity[all_cities.index(city)]
        body.append(item_template.format(city, mintensity))
    # for mi in mean_intensity:
    #     body.append(item_template.format(mi))
    body.append('</ul>')
    return '\n'.join(body)
    # return mean_intensity


def city(city):
    body = '<h1>{City}</h1>, <table>'
    item_template = ("""
    <tr><th><strong>Time/Date:</th><td>{timedate}</strong></td></tr>
    <tr><th>Distance from {city}:</th><td>{city_distance}</td></tr>
    <tr><th>Depth Distance from {city}:</th><td>{depth_dist}</td></tr>
    <tr><th>Magnitude:</th><td>{magnitude}</td></tr>
    <tr><th>Intensity:</th><td>{mintensity}</td></tr>
    """)
    all_cities = [key for key in temp_dict]
    mean_intensity = [temp_dict[city][0] for city in all_cities]
    for city in all_cities:
        mintensity = mean_intensity[all_cities.index(city)]
        timedate = [temp_dict[city][1][0]
        city_distance = [temp_dict[city][1][1]
        depth_dist = [temp_dict[city][1][2]
        magnitude = [temp_dict[city][1][3]
        body.append(item_template.format(city, timedate, city_distance,
                    depth_dist, magnitude, mintensity))
    number_of_events = [len(temp_dict.keys()[city]) for city in all_cities]
    body.append('<a href="/">Back to the list</a>')
    return '\n'.join(body)

    if city is None:
        raise NameError
    return page.format(**city)


def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    # import pdb; pdb.set_trace()
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
    # earthquake()
    # if len(sys.argv) > 1 and sys.argv[1] == 'test':
    #     html, encoding = read_search_results()
    # else:
    # pprint(cities())
    # pprint(earthquake())
