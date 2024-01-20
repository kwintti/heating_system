import plotly.express as px
from db_connect import talk_to_db
from plotly.subplots import make_subplots
import plotly.graph_objects as go

outside_temp_48h = talk_to_db(getting_data=True, table_name="out_temp", row_nums=48)
energy_prices_48h = talk_to_db(getting_data=True, table_name="energy_price", row_nums=48)

out_x = []
out_y = []

energy_x = []
energy_y = []

for value in energy_prices_48h:
    energy_x.append(value[0])
    energy_y.append(float(value[1]))

for value in outside_temp_48h:
    out_x.append(value[0])
    out_y.append(float(value[1]))

fig = make_subplots(rows=1, cols=2)

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
#fig = px.line(x=out_x, y=out_y)
fig.write_html('web_graphs/temp_outside_48h.html', auto_open=True)
