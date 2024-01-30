from make_graphs import getting_data_from_db
import numpy as np
import datetime
from db_connect import talk_to_db

out_x, out_y, energy_x, energy_y, room_x, room_y, avg_prices = getting_data_from_db()

# We get two hour of cheapest energy prices for 48 hours and plan our boiler on time during them. We need two hours to warm water up.
connect_prices = list(zip(energy_x, energy_y))
prices_sorted = sorted(connect_prices, key=lambda x: x[1])
top_two_cheapest_hours = prices_sorted[:2]


def schedule_boiler():
    # If prices are very high, we will check our room_temp and if it is over 19 we try to postpone warming up of our heating system.
    schedule_for_boiler = []
    for h in range(0, 24):
        hour_now = datetime.datetime.combine(datetime.datetime.utcnow(), datetime.time.min) + datetime.timedelta(hours=h) + datetime.timedelta(days=1)
        hour_now = hour_now.replace(tzinfo=datetime.timezone.utc)
        schedule_for_boiler.append((str(hour_now), False))
        for d, p in top_two_cheapest_hours:
            if hour_now == datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S%z"):
                schedule_for_boiler = schedule_for_boiler[:-1]
                schedule_for_boiler.append((str(hour_now), True))

    for tup in schedule_for_boiler:
        talk_to_db(boi_date=tup[0], boi_on=tup[1])


# Check avg room temp
avg_room_temp = np.average(room_y)

# Lets calculate simple moving average for energy prices, so we know the trend

i=0
moving_averages = []
while i < len(avg_prices) - 4:
    window_average = round(np.sum(avg_prices[i:i+3]) / 3, 2)
    moving_averages.append(window_average)
    i += 1
final_moving_avg = moving_averages[-1:][0]

# Logic is following: if cheapest hours are higher than SMA, postpone boiler but if room temp is under 19, put it on anyway
for d, p in top_two_cheapest_hours:
    if p > final_moving_avg:
        if avg_room_temp < 19:
            schedule_boiler()
            break
    else:
        schedule_boiler()
        break

def turn_boiler_on():
    print("Boiler is on.")
