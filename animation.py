import pandas as pd
import numpy as np
import requests
from utils import load_scifi_table

def get_geocode(location):
    """Returns tuple of longitude and latitude of a given location"""

    if location is np.nan:
        return np.nan, np.nan

    address_splitted = location.split(" ")
    address_splitted = [x.strip() for x in address_splitted]
    address = "+".join(address_splitted)
    url = ("http://www.datasciencetoolkit.org/maps/api/geocode/json?sensor=false"
           "&address={}").format(address)

location = "Warsaw, Poland"   
address_splitted = location.split(" ")
address_splitted = [x.strip() for x in address_splitted]
address = "+".join(address_splitted)
url = ("http://www.datasciencetoolkit.org/maps/api/geocode/json?sensor=false"
       "&address={}").format(address)
r = requests.get(url)
print(r)

    

