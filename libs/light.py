from datetime import datetime
from suntime import Sun
from geopy.geocoders import Nominatim


def get_sun_set_rise(place):
    # Nominatim API to get latitude and longitude
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(place)
    # latitude and longitude fetch
    latitude = location.latitude
    longitude = location.longitude
    sun = Sun(latitude, longitude)
    # date in your machine's local time zone
    time_zone = datetime.now()
    sun_rise = sun.get_local_sunrise_time(time_zone)
    sun_dusk = sun.get_local_sunset_time(time_zone)
    return sun_rise, sun_dusk

def day_or_night(place):
    sun_rise, sun_dusk = get_sun_set_rise(place)
    if datetime.now() < sun_rise:
        light_status = 0
    elif datetime.now() > sun_rise and datetime.now() < sun_dusk:
        light_status = 1
    elif datetime.now() > sun_dusk:
        light_status = 0
    return light_status

if __name__ == '__main__':
    place = "brussels"
    light = day_or_night(place)