import pandas as pd
import numpy as np
import requests
from utils import load_scifi_table


def return_na(get_country, get_city):
    if get_country:
        if get_city:
            return tuple(np.nan for _ in range(4))
        else:
            return tuple(np.nan for _ in range(3))
    else:     
        return np.nan, np.nan


def get_location_data(location, get_country=False, get_city=False, verbose=False):
    """Returns location data (geographical coordinates and country and city)
    * lattitude, longitude, country, city if get_country and get_city are True
    * lattitude, longitude, country if only get_country is True
    * lattitude, longitude otherwise
    """
    if verbose:
        print(location)

    if location is np.nan:
        return return_na(get_country, get_city)
    try:
        address_splitted = location.split(" ")
        address_splitted = [x.strip() for x in address_splitted]
        address = "+".join(address_splitted)
        url = ("http://www.datasciencetoolkit.org/maps/api/geocode/json?sensor=false"
            "&address={}").format(address)

        r = requests.get(url)
        result = r.json()['results']
        if not result:
            return return_na(get_country, get_city)

        coordinates = result[0]["geometry"]["location"]

        country, city = np.nan, np.nan
        if get_country or get_city:
            address_components = result[0]['address_components']
            for component in address_components:
                if 'country' in component['types']: 
                    country = component['long_name']
                    # Unfortunately, sometimes country can be empty string, 
                    # for example for location == "Europe"
                elif 'locality' in component['types']:
                    city = component['short_name']

        if get_country:
            if get_city:
                return coordinates['lat'], coordinates['lng'], country, city
            else:
                return coordinates['lat'], coordinates['lng'], country
        else:     
            return coordinates['lat'], coordinates['lng']

    except KeyboardInterrupt:
        raise KeyboardInterrupt

    except Exception as exc:
        print("!!!Exception of type {} on location {}".format(str(exc), location))
        return_na(get_country, get_city)


def get_geocode(location):
    """Returns tuple of latitude and longitude for a given location"""
    return get_location_data(location, False, False)


### Code for debugging purposes
# location = "Europe"
# address_splitted = location.split(" ")
# address_splitted = [x.strip() for x in address_splitted]
# address = "+".join(address_splitted)
# url = ("http://www.datasciencetoolkit.org/maps/api/geocode/json?sensor=false"
#         "&address={}").format(address)

# r = requests.get(url)
# result = r.json()['results']


# coordinates = result[0]["geometry"]["location"]

# country, city = np.nan, np.nan
# if True:
#     address_components = result[0]['address_components']
#     for component in address_components:
#         if 'country' in component['types']:
#             country = component['long_name']
#         elif 'locality' in component['types']:
#             city = component['short_name']