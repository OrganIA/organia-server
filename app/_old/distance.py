from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="Organia")


def get_coordinates(address):
    location = geolocator.geocode(address)
    if not location:
        return None
    position = (location.latitude, location.longitude)
    return position


def get_distance(pos_1, pos_2):
    if pos_1 is None or pos_2 is None:
        raise Exception("Fill both fields.")
    try:
        distance = geodesic(get_coordinates(pos_1), get_coordinates(pos_2)).km
        return distance
    except Exception as e:
        raise Exception("One of these addresses is not correct.") from e
