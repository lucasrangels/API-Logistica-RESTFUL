from geopy.geocoders import Nominatim

app_name = 'logistics_app'


def get_coordinates_by_location(address):
    locator = Nominatim(user_agent=app_name)
    geo_return = locator.geocode(address)
    if not geo_return:
        return False
    else:
        return geo_return.longitude, geo_return.latitude


def get_location_by_coordinates(lat_long):
    locator = Nominatim(user_agent=app_name)
    geo_return = locator.reverse(lat_long)
    if not geo_return:
        return False
    else:
        return geo_return.address
