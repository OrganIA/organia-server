from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="my_request")


def get_coordinates(address):
    location = geolocator.geocode(address)
    position = [location.latitude, location.longitude]
    return position


def get_distance(address_1, address_2):
    distance = geodesic(get_coordinates(address_1), get_coordinates(address_2))
    return distance
