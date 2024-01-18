from fmiopendata.wfs import download_stored_query
from db_connect import *

data = download_stored_query("fmi::forecast::harmonie::surface::point::multipointcoverage", ["place=espoo"])
for time in data.data.keys():
    deg = data.data[time]["Espoo"]["Air temperature"]["value"]
    talk_to_db(time, deg)
