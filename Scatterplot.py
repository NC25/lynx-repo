from dash import Dash, dcc, html
import numpy as np
import pandas as pd
import plotly.express as px

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

stats1 = pd.read_html("player-data/WNBA Stats _ Players Bios1.html", flavor = "lxml")
stats2 = pd.read_html("player-data/WNBA Stats _ Players Bios2.html", flavor = "lxml")
stats3 = pd.read_html("player-data/WNBA Stats _ Players Bios3.html", flavor = "lxml")
stats4 = pd.read_html("player-data/WNBA Stats _ Players Bios4.html", flavor = "lxml")
stats_total = pd.concat([stats1[0], stats2[0], stats3[0], stats4[0]])
stats_total = stats_total.reset_index()[["Player", "Age"]]

all_players = pd.read_csv("all_players.csv")
all_players.sort_values(by = "PLAYER")

stats_total["Player"] = stats_total["Player"].astype(str)
all_players["PLAYER"] = all_players["PLAYER"].astype(str)
all_players["PLAYER"] = all_players["PLAYER"].str.split().str.join(' ')


merged = pd.merge(left = stats_total, right = all_players, left_on = "Player", right_on = "PLAYER")
for year in range(2023, 2027):
    merged[str(year)] = merged[str(year)].str.replace(",", "").str.extract('\$(.*)').astype(float)
merged.to_csv("merged.csv")
merged = merged.sort_values("TEAM")

year_grouped = merged.groupby("TEAM")[["2023", "2024", "2025", "2026"]].sum().T
year_grouped["League Average"] = year_grouped.aggregate(func = np.mean, axis = 1)


# ----------------- PLOT GENERATION ----------------- #

color_sequence = ["#C8102E",
                  "#418FDE",
                  "#DC4405",
                  "#C4D600",
                  "#FFCD00",
                  "#85714D",
                  "#702F8A",
                  "#236192",
                  "#6ECEB2",
                  "#CB6015",
                  "#2C5234",
                  "#C8102E",
                  "black"]

ages_fig = px.scatter(merged, x="Age",
                 y="2023",
                 color = "TEAM",
                 hover_data = ["Player"],
                 trendline = "lowess",
                 trendline_scope = "overall",
                 title = "Age vs WNBA 2023 Salary",
                 color_discrete_sequence=color_sequence,
                 labels = {"2023": "2023 Player Salary", "TEAM": "Team"},
                 trendline_options=dict(frac=0.5))

year_fig = px.line(year_grouped,
              title="Team Salary Over Time",
              x= year_grouped.index,
              y=year_grouped.columns[:],
              color_discrete_sequence = color_sequence,
              labels={'index': 'Year', 'value':'Salary Commitments', "variable": "Team"})
for n in range(12):
    year_fig['data'][n]['line']['width']=1
year_fig['data'][12]['line']['width']=3


# ----------------- DASHBOARD LAYOUT ----------------- #


app.layout = html.Div(children = [
    html.H1(children= '''
    WNBA Salaries
    '''),

    html.Div(children = [dcc.Graph(id = 'Total-age-graph',figure = ages_fig),
                         dcc.Graph(id = 'Total-years-graph', figure = year_fig)
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)