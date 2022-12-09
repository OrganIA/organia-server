from geopy.distance import geodesic
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="NewOrganiaa")


def get_coordinates(address):
    location = geolocator.geocode(address)
    if not location:
        return []
    position = [location.latitude, location.longitude]
    return position


def get_distance(pos_1, pos_2):
    return geodesic(get_coordinates(pos_1), get_coordinates(pos_2)).km
