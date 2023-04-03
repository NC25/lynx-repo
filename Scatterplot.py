from dash import Dash, dcc, html
import pandas as pd

app = Dash(__name__)

# --------------- TABLE FORMATTING --------------- #

atl = pd.read_csv("team-data/Atlanta Dream (1).csv")
chi = pd.read_csv("team-data/Chicago Sky.csv")
con = pd.read_csv("team-data/Connecticut Sun.csv")
dal = pd.read_csv("team-data/Dallas Wings (1).csv")
ind = pd.read_csv("team-data/Indiana Fever.csv")
lav = pd.read_csv("team-data/Las Vegas Aces (2).csv")
la = pd.read_csv("team-data/Los Angeles Sparks.csv")
min = pd.read_csv("team-data/Minnesota Lynx (1).csv")
ny = pd.read_csv("team-data/New York Liberty (2).csv")
pho = pd.read_csv("team-data/Phoenix Mercury.csv")
sea = pd.read_csv("team-data/Seattle Storm.csv")
was = pd.read_csv("team-data/Washington Mystics.csv")

ages_pg1 = pd.read_html("player-data/WNBA Stats _ Players Bios1.html")
ages_pg2 = pd.read_html("player-data/WNBA Stats _ Players Bios2.html")
ages_pg3 = pd.read_html("player-data/WNBA Stats _ Players Bios3.html")
ages_pg4 = pd.read_html("player-data/WNBA Stats _ Players Bios4.html")

ages = pd.concat([ages_pg1[0], ages_pg2[0], ages_pg3[0], ages_pg4[0]]).reset_index()

# ----------------- DASHBOARD LAYOUT ----------------- #

app.layout = html.Div([
    html.Div(children='Hello World')
])

if __name__ == '__main__':
    app.run_server(debug=True)