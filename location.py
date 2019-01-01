import pandas as pd
import numpy as np
import requests
from utils import load_scifi_table

def get_geocode(location):
    """Returns tuple of latitude and longitude of a given location"""

    if location is np.nan:
        return np.nan, np.nan

    address_splitted = location.split(" ")
    address_splitted = [x.strip() for x in address_splitted]
    address = "+".join(address_splitted)
    url = ("http://www.datasciencetoolkit.org/maps/api/geocode/json?sensor=false"
           "&address={}").format(address)

    r = requests.get(url)
    result = r.json()['results']
    if not result:
        return np.nan, np.nan
    coordinates = result[0]["geometry"]["location"]

    return coordinates['lat'], coordinates['lng']

