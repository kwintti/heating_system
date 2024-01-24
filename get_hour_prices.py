import requests
import zoneinfo
import datetime
from db_connect import talk_to_db

url = "https://api.porssisahko.net/v1/latest-prices.json"
res = requests.get(url)
to_json = res.json()
data_to_db = []

latest_date = talk_to_db(fetch=True, table_name="energy_price")
latest_date_to_dateformat = datetime.datetime.fromisoformat(latest_date)

for value in to_json["prices"]:
    data_to_db.insert(0, (datetime.datetime.fromisoformat(value["startDate"]), value["price"]))

for val in data_to_db:
    if val[0] > latest_date_to_dateformat:
        talk_to_db(eng_date=val[0], eng_price=val[1])


#dt = datetime(date, tzinfo=zoneinfo.Zoneinfo("Europe/Helsinki"))
