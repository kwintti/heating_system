from db_connect import talk_to_db
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def getting_data_from_db():
    outside_temp_48h = talk_to_db(getting_data=True, table_name="out_temp", row_nums=48)
    energy_prices_48h = talk_to_db(getting_data=True, table_name="energy_price", row_nums=48)
    room_temp = talk_to_db(getting_data=True, table_name="room_temp", row_nums=48)
    avg_prices_y = talk_to_db(getting_data=True, table_name="avg_prices", row_nums=12)

    out_x = []
    out_y = []

    energy_x = []
    energy_y = []

    room_x = []
    room_y = []

    avg_prices = []

    for value in energy_prices_48h:
        energy_x.append(value[0])
        energy_y.append(float(value[1]))

    for value in outside_temp_48h:
        out_x.append(value[0])
        out_y.append(float(value[1]))

    for value in room_temp:
        room_x.append(value[0])
        room_y.append(float(value[1]))

    for value in avg_prices_y:
        avg_prices.append(float(value[1]))

    return out_x, out_y, energy_x, energy_y, room_x, room_y, avg_prices


out_x, out_y, energy_x, energy_y, room_x, room_y, avg_prices = getting_data_from_db()

if __name__ == "__main__":
    fig = make_subplots(rows=2, cols=2)

    fig.add_scatter(x=out_x, y=out_y,
                    row=1,
                    col=1,
                    name="Temp outside"
                    )
    fig.add_scatter(x=energy_x, y=energy_y,
                    row=1,
                    col=2,
                    name="Energy price"
                    )
    fig.add_scatter(x=room_x, y=room_y,
                    row=2,
                    col=1,
                    name="Temp inside"
                    )

    #fig2.add_trace(go.Table(header=dict(values=['A Scores', 'B Scores']),
    #                 cells=dict(values=[[100, 90, 80, 90], [95, 85, 75, 95]])))
    #fig.add_trace(go.Indicator(
    #    mode="number",
    #    value=14.5,
    #    domain={"y": [0, 1], "x": [0.25, 0.75]}))

    fig.update_layout(hovermode="x unified")
    fig.write_html('web_graphs/temp_outside_48h.html', auto_open=True)
