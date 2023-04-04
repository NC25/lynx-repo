from dash import Dash, dcc, html, dash_table
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

teams = [atl, chi, con, dal, ind, lav, la, min, ny, pho, sea, was]

bios_pg1 = pd.read_html("player-data/WNBA Stats _ Players Bios1.html")
bios_pg2 = pd.read_html("player-data/WNBA Stats _ Players Bios2.html")
bios_pg3 = pd.read_html("player-data/WNBA Stats _ Players Bios3.html")
bios_pg4 = pd.read_html("player-data/WNBA Stats _ Players Bios4.html")

ages = pd.concat([bios_pg1[0], bios_pg2[0], bios_pg3[0], bios_pg4[0]]).reset_index()

gg = 11

# ----------------- DASHBOARD LAYOUT ----------------- #

app.layout = dash_table.DataTable(atl.to_dict('records'), [{"name": i, "id": i} for i in atl.columns])

if __name__ == '__main__':
    app.run_server(debug=True)