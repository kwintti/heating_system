from fmiopendata.wfs import download_stored_query
from db_connect import talk_to_db
import datetime

data = download_stored_query("fmi::forecast::harmonie::surface::point::multipointcoverage", ["place=espoo"])
latest_date = talk_to_db(fetch=True, table_name="out_temp")
latest_date_to_dateformat = datetime.datetime.strptime(latest_date, "%Y-%m-%d %H:%M:%S")
time_now = datetime.datetime.now()
for time in data.data.keys():
    deg = data.data[time]["Espoo"]["Air temperature"]["value"]
    # Only add new values to the database
    if time > latest_date_to_dateformat:
        talk_to_db(time, deg)
