# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

bios_pg1 = pd.read_html("player-data/WNBA Stats _ Players Bios1.html")
bios_pg2 = pd.read_html("player-data/WNBA Stats _ Players Bios2.html")
bios_pg3 = pd.read_html("player-data/WNBA Stats _ Players Bios3.html")
bios_pg4 = pd.read_html("player-data/WNBA Stats _ Players Bios4.html")

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv("all_players")

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H2(children='Scatter'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
