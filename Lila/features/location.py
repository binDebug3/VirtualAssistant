import webbrowser
import requests
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import geocoder

def location(place):
    webbrowser.open("https://www.google.com/maps/place/" + place + "")
    geolocator = Nominatim(user_agent="myGeocoder", timeout=5)
    location = geolocator.geocode(place, addressdetails=True)

    target_latlng = location.latitude, location.longitude
    location = location.raw['address']
    target_loc = {'city': location.get('city', ''),
                   'state': location.get('state', ''),
                   'country': location.get('country', '')}

    current_loc = geocoder.ip('me')
    current_latlng = current_loc.latlng

    distance = round(float(str(str(great_circle(current_latlng, target_latlng)).split(' ', 1)[0])), 2)

    return current_loc, target_loc, distance


def my_location():
    ip_add = requests.get("https://api.ipify.org").text
    url = 'https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'
    geo_requests = requests.get(url)
    geo_data = geo_requests.json()
    city = geo_data['city']
    state = geo_data['region']
    country = geo_data['country']

    return city, state, country