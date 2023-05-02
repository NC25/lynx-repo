from dash import Dash, dcc, html
import numpy as np
import pandas as pd
import plotly.express as px

app = Dash(__name__)

# --------------- TABLE FORMATTING --------------- #

# Present Player Salary Data
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

# Array of team DataFrames
team_tables = [atl, chi, con, dal, ind, lav, la, min, ny, pho, sea, was]

# Web Scraped Age Data
stats1 = pd.read_html("player-data/WNBA Stats _ Players Bios1.html", flavor = "lxml")
stats2 = pd.read_html("player-data/WNBA Stats _ Players Bios2.html", flavor = "lxml")
stats3 = pd.read_html("player-data/WNBA Stats _ Players Bios3.html", flavor = "lxml")
stats4 = pd.read_html("player-data/WNBA Stats _ Players Bios4.html", flavor = "lxml")
stats_total = pd.concat([stats1[0], stats2[0], stats3[0], stats4[0]])
stats_total = stats_total.reset_index()[["Player", "Age"]]

# DataFrame of all salary data
all_players = pd.read_csv("all_players.csv")
all_players.sort_values(by = "PLAYER")

# Format cleaning to ensure DataFrame merging works
stats_total["Player"] = stats_total["Player"].astype(str)
all_players["PLAYER"] = all_players["PLAYER"].astype(str)
all_players["PLAYER"] = all_players["PLAYER"].str.split().str.join(' ')

# Merge age data with player salary data
merged = pd.merge(left = stats_total, right = all_players, left_on = "Player", right_on = "PLAYER")
for year in range(2023, 2027):
    merged[str(year)] = merged[str(year)].str.replace(",", "").str.extract('\$(.*)').astype(float)
merged.to_csv("merged.csv")
merged = merged.sort_values("TEAM")

# Group data by team for lineplot
year_grouped = merged.groupby("TEAM")[["2023", "2024", "2025", "2026"]].sum().T

def data_cleaning(df):
    copy = df.copy()
    copy.columns = copy.iloc[1, :]
    copy = copy.drop([0, 1], axis=0).reset_index(drop=True)
    return copy.iloc[:len(copy) - 5, :]

# List of team labels to iterate through for historical data
teams = ["ATL", "CHI", "CON", "DAL", "IND", "LVA", "LAS", "MIN", "NYL", "PHO", "SEA", "WAS"]

full_team_names = {"ATL": "Atlanta Dream",
                   "CHI": "Chicago Sky",
                   "CON": "Connecticut Sun",
                   "DAL": "Dallas Wings",
                   "IND": "Indiana Fever",
                   "LVA": "Las Vegas Aces",
                   "LAS": "Los Angeles Sparks",
                   "MIN": "Minnesota Lynx",
                   "NYL": "New York Liberty",
                   "PHO": "Phoenix Mercury",
                   "SEA": "Seattle Storm",
                   "WAS": "Washington Mystics"}

# Read Excel sheets
xlxs_years = {}
for year in np.arange(2014, 2022, 1):
    xlxs_years[year] = pd.ExcelFile("historical-data/" + str(year) + ".xlsx")

# Create DataFrame for all historical team data
hist_team_stats = pd.DataFrame()
for team in teams:
    data = []
    for year in np.arange(2014, 2022, 1):
        year_sheet = xlxs_years[year]
        team_year_data_uncleaned = pd.read_excel(year_sheet, team)
        team_year_data = data_cleaning(team_year_data_uncleaned)
        data += [team_year_data[year]]
    hist_team_stats = pd.concat([hist_team_stats, pd.DataFrame(pd.DataFrame(data).T.fillna(0).sum(), columns=[full_team_names[team]])], axis=1)


# ----------------- PLOT GENERATION ----------------- #

colors = {
    'background': '#061A33',
    'graph background': '#021429',
    'text': '#FFFFFF'
}

color_sequence = ["#CED9E5",
                  "#418FDE",
                  "#DC4405",
                  "#DBEE05",
                  "#FFCD00",
                  "#E9C585",
                  "#702F8A",
                  "#236192",
                  "#6ECEB2",
                  "#CB6015",
                  "#4F975E",
                  "#C8102E"]

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

curr_salary_fig = px.line(year_grouped,
              title="Present Team Salary Commitments Over Time",
              x= year_grouped.index,
              y=year_grouped.columns[:],
              color_discrete_sequence = color_sequence,
              labels={'index': 'Year', 'value':'Salary Commitments', "variable": "Team"})
for n in range(12):
    curr_salary_fig['data'][n]['line']['width']=1

hist_salary_fig = px.line(hist_team_stats,
                   title="Historical Team Salary Trends",
                   x= hist_team_stats.index,
                   y=hist_team_stats.columns[:],
                   labels={'index': 'Year', 'value':'Salary Commitments', 'variable': 'Team'},
                   color_discrete_sequence=color_sequence)
for n in range(12):
    hist_salary_fig['data'][n]['line']['width']=1


# ----------------- DASHBOARD LAYOUT ----------------- #

ages_fig.update_layout(
    plot_bgcolor=colors['graph background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

curr_salary_fig.update_layout(
    plot_bgcolor=colors['graph background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

hist_salary_fig.update_layout(
    plot_bgcolor=colors['graph background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)


app.layout = html.Div(style={'backgroundColor': colors['background']}, children = [
    html.H1(children= 'WNBA Salary Plots',
            style={
                'textAlign': 'center',
                'color': colors['text'],
                'fontSize':50,
                'font-family':'sans-serif'
            }),

    html.Div(children = [dcc.Graph(id = 'Age-graph',figure = ages_fig),
                         dcc.Graph(id = 'Current-Salary-graph', figure = curr_salary_fig),
                         dcc.Graph(id = 'Historical-Salary-graph', figure = hist_salary_fig)
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)