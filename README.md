Mashup
======

By [jwhite007](https://github.com/jwhite007/) and [lhp81](https://github.com/lhp1981/) for [Cris Ewing](https://github.com/cewing/) at [CodeFellows](http://codefellows.org/)

This script uses the API from [Seismi](http://www.seismi.org/), mashed up with geocoding data from Google Maps.

Data is pulled from Seismi about all 7.0+ magnitude earthquakes that happened in 2013. Data pulled includes longitude, latitude, time/date, magnitude (Richter), and depth.

Google Maps data is used to call long/lat data for major west coast cities (Seattle, Vancouver, Portland, SF, LA), and the script then uses this data to calculate the **distance** of the earthquake from each of the cities (km), the **distance depth** of the earthquake from each of the cities (km), and the **intensity** of the effect of the earthquake felt in each of the cities(10,000 x magnitude / depth distance).

This data is collocated and published automatically.



Requirements:
beautifulsoup4
html5lib
requests
six
wsgiref
