import plotly.express as px
from db_connect import talk_to_db

outside_temp_48h = talk_to_db(getting_data=True, row_nums=48)

x = []
y = []

for value in outside_temp_48h:
    x.append(value[0])
    y.append(value[1])

fig = px.line(x=x, y=y)
fig.write_html('web_graphs/temp_outside_48h.html', auto_open=True)
