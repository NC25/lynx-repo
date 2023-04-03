from dash import Dash, dcc, html
import pandas as pd

app = Dash(__name__)

atl = pd.read_csv("team-data/Atlanta Dream(1).csv")
chi = pd.read_csv("team-data/Chicago Sky.csv")
con = pd.read_csv("team-data/Connecticut Sun.csv")
dal = pd.read_csv("team-data/Dallas Wings (1).csv")
ind = pd.read_csv("team-data/Indiana Fever.csv")
lav = pd.read_csv("team-data/Las Vegas Aces (2).csv")
la = pd.read_csv("team-data/Los Angeles Sparks.csv")
min = pd.read_csv("team-data/Minnesota Lynx (1).csv")
ny = pd.read_csv("team-data/New York Liberty (2).csv")
pho = pd.read_csv("team-data/Phoneix Mercury.csv")
sea = pd.read_csv("team-data/Seattle Storm.csv")
was = pd.read_csv("team-data/Washington Mystics.csv")


app.layout = html.Div([
    html.Div(children='Hello World')
])

if __name__ == '__main__':
    app.run_server(debug=True)