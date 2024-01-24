from make_graphs import getting_data_from_db
import numpy as np
import datetime
from db_connect import talk_to_db

out_x, out_y, energy_x, energy_y, room_x, room_y = getting_data_from_db()

# We get 1st precintile of energy prices for 48 hours and plan our boiler on time during them. We need two hours to warm water up.
#bottom_25 = np.percentile(energy_y, 25)
#lowest_price_hours = [(x, y) for y, x in zip(energy_y, energy_x) if y <= bottom_25]
connect_prices = list(zip(energy_x, energy_y))
prices_sorted = sorted(connect_prices, key=lambda x: x[1])
top_two_cheapest_hours = prices_sorted[:2]

# If prices are very high, we will check our room_temp and if it is over 19 we try to postpone warming up of our heating system.
schedule_for_boiler = []
for h in range(0, 24):
    hour_now = datetime.datetime.combine(datetime.datetime.utcnow(), datetime.time.min) + datetime.timedelta(hours=h)
    hour_now = hour_now.replace(tzinfo=datetime.timezone.utc)
    schedule_for_boiler.append((str(hour_now), False))
    for d, p in top_two_cheapest_hours:
        if hour_now == datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S%z"):
            schedule_for_boiler = schedule_for_boiler[:-1]
            schedule_for_boiler.append((str(hour_now), True))
for tup in schedule_for_boiler:
    talk_to_db(boi_date=tup[0], boi_on=tup[1])
#for val in zip(energy_x, energy_y):
#    print(val)
def turn_boiler_on():
    print("Boiler is on.")
