import requests
import datetime
from db_connect import talk_to_db
import numpy as np
import pandas as pd
from make_graphs import getting_data_from_db

# We get data for the next day after 14:00 Helsinki time.
url = "https://api.porssisahko.net/v1/latest-prices.json"
res = requests.get(url)
to_json = res.json()
data_to_db = []

latest_date = talk_to_db(fetch=True, table_name="energy_price")
latest_date_to_dateformat = datetime.datetime.fromisoformat(latest_date)
latest_date_to_dateformat = latest_date_to_dateformat.replace(tzinfo=datetime.timezone.utc)

for value in to_json["prices"]:
    data_to_db.insert(0, (datetime.datetime.fromisoformat(value["startDate"]), value["price"]))


for val in data_to_db:
    if val[0] > latest_date_to_dateformat:
        talk_to_db(eng_date=val[0], eng_price=val[1])

def calculate_avg_price():
    _, _, energy_x, energy_y, _, _ = getting_data_from_db()
    df_raw = zip(energy_x, energy_y)
    df = pd.DataFrame(df_raw, columns=['days', 'price'])
    df['days'] = pd.to_datetime(df['days'])
    df['days'] = df['days'].dt.strftime("%Y-%m-%d")
    table = pd.pivot_table(df, values='price', index='days', aggfunc='mean')
    latest_entery_avg_price = talk_to_db(fetch=True, table_name="avg_prices")
    if latest_entery_avg_price is not None:
        latest_entery_avg_price_dateformat = datetime.datetime.strptime(latest_entery_avg_price, "%Y-%m-%d")
    for index, row in table.iterrows():
        date = datetime.datetime.strptime(index, "%Y-%m-%d")
        if latest_entery_avg_price is None or latest_entery_avg_price_dateformat and date > latest_entery_avg_price_dateformat:
            talk_to_db(avg_date=index, avg_price=round(row['price'], 3))
calculate_avg_price()

date_now = datetime.datetime.combine(datetime.datetime.utcnow(), datetime.time.min)
date_now = date_now.replace(tzinfo=datetime.timezone.utc)
date_yesterday = date_now - datetime.timedelta(days=1)
#dt = datetime(date, tzinfo=zoneinfo.Zoneinfo("Europe/Helsinki"))
