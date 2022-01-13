from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="my_request")

def get_coordinates(address):
    location = geolocator.geocode(address)
    position = [location.latitude, location.longitude]
    return position

def get_distance(first_address, second_address):
    distance = geodesic(get_coordinates(first_address), get_coordinates(second_address))
    return distance