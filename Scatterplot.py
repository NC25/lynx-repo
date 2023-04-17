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

teams = [atl, chi, con, dal, ind, lav, la, min, ny, pho, sea, was]

ages1 = pd.read_html("player-data/WNBA Stats _ Players Bios1.html", flavor = "lxml")
ages2 = pd.read_html("player-data/WNBA Stats _ Players Bios2.html", flavor = "lxml")
ages3 = pd.read_html("player-data/WNBA Stats _ Players Bios3.html", flavor = "lxml")
ages4 = pd.read_html("player-data/WNBA Stats _ Players Bios4.html", flavor = "lxml")
ages = pd.concat([ages1[0], ages2[0], ages3[0], ages2[0]])
ages = ages.reset_index()[["Player", "Age"]]

all_players = pd.read_csv("all_players.csv")
all_players.sort_values(by = "PLAYER")

ages["Player"] = ages["Player"].astype(str)
all_players["PLAYER"] = all_players["PLAYER"].astype(str)
all_players["PLAYER"] = all_players["PLAYER"].str.split().str.join(' ')
merged = pd.merge(left = ages, right = all_players, left_on = "Player", right_on = "PLAYER")
merged["2023 Salary"] = merged["2023"].str.replace(",", "").str.extract('\$(.*)').astype(float)
merged.to_csv("merged.csv")
merged = merged.sort_values("2023 Salary", ascending=False)

# ----------------- DASHBOARD LAYOUT ----------------- #

import plotly.express as px

fig = px.scatter(merged, x="Age", y="2023 Salary", color = "TEAM", hover_data = ["Player"], trendline = "lowess", trendline_scope = "overall", title = "Age vs WNBA 2023 Salary", trendline_options=dict(frac=0.5))
fig.show()