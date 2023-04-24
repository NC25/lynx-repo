# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output, State
from dash import no_update
import pandas as pd

teams = ['Atlanta Dream', 'Chicago Sky', 'Connecticut Sun', 'Dallas Wings', 'Indiana Fever', 'Las Vegas Aces', 'Los Angeles Sparks', 'Minnesota Lynx', 'New York Liberty', 'Phoenix Mercury', 'Seattle Storm', 'Washington Mystics']


teams_columns = ['PLAYER', '2023 TYPE', '2023', '2024 TYPE', '2024', '2025 TYPE', '2025', '2026 TYPE', '2026', '2027 TYPE', '2027', 'TEAM']

teams_dict = {'Atlanta Dream':'team-data/Atlanta Dream.csv', 'Chicago Sky':'team-data/Chicago Sky.csv', 'Connecticut Sun':'team-data/Connecticut Sun.csv', 'Dallas Wings':'team-data/Dallas Wings.csv', 'Indiana Fever':'team-data/Indiana Fever.csv', 'Las Vegas Aces':'team-data/Las Vegas Aces.csv', 'Los Angeles Sparks':'team-data/Los Angeles Sparks.csv', 'Minnesota Lynx':'team-data/Minnesota Lynx.csv', 'New York Liberty':'team-data/New York Liberty.csv', 'Phoenix Mercury':'team-data/Phoenix Mercury.csv', 'Seattle Storm':'team-data/Seattle Storm.csv', 'Washington Mystics':'team-data/Washington Mystics.csv'   
}

# df1 = pd.read_csv(teams_dict['Atlanta Dream'], usecols=teams_columns)
# df1 = df1.iloc[:18].drop([15,16])
# df1['Team'] = teams[0]
# df2 = pd.read_csv(teams_dict['Chicago Sky'], usecols=teams_columns)
# df2 = df2.iloc[:22].drop([19,20])
# df2['Team'] = teams[1]
# df3 = pd.read_csv(teams_dict['Connecticut Sun'], usecols=teams_columns)
# df3 = df3.iloc[:20].drop([17,18])
# df3['Team'] = teams[2]
# df4 = pd.read_csv(teams_dict['Dallas Wings'], usecols=teams_columns)
# df4 = df4.iloc[:16].drop([13,14])
# df4['Team'] = teams[3]
# df5 = pd.read_csv(teams_dict['Indiana Fever'], usecols=teams_columns)
# df5 = df5.iloc[:20].drop([17,18])
# df5['Team'] = teams[4]
# df6 = pd.read_csv(teams_dict['Las Vegas Aces'], usecols=teams_columns)
# df6 = df6.iloc[:17].drop([14,15])
# df6['Team'] = teams[5]
# df7 = pd.read_csv(teams_dict['Los Angeles Sparks'], usecols=teams_columns)
# df7 = df7.iloc[:20].drop([17,18])
# df7['Team'] = teams[6]
# df8 = pd.read_csv(teams_dict['Minnesota Lynx'], usecols=teams_columns)
# df8 = df8.iloc[:20].drop([17,18])
# df8['Team'] = teams[7]
# df9 = pd.read_csv(teams_dict['New York Liberty'], usecols=teams_columns)
# df9 = df9.iloc[:19].drop([16,17])
# df9['Team'] = teams[8]
# df10 = pd.read_csv(teams_dict['Phoenix Mercury'], usecols=teams_columns)
# df10 = df10.iloc[:17].drop([14,15])
# df10['Team'] = teams[9]
# df11 = pd.read_csv(teams_dict['Seattle Storm'], usecols=teams_columns)
# df11 = df11.iloc[:20].drop([17,18])
# df11['Team'] = teams[10]
# df12 = pd.read_csv(teams_dict['Washington Mystics'], usecols=teams_columns)
# df12 = df12.iloc[:20].drop([17,18])
# df12['Team'] = teams[11]

# frames = [df1,df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12]
years = ['2023', '2024', '2025', '2026', '2027']
# df = pd.concat(frames)
df = pd.read_csv('team-data/All Teams Pie.csv', usecols=teams_columns)

# df = df.astype({'2023':'string','2024':'string','2025':'string','2026':'string','2027':'string'})
def format(x):
    if (str(x) == 'nan'):
        return 0
    return int(x)
for i in years:
    df[i] = df[i].map(format)

app = Dash(__name__)


app.layout = html.Div([
    html.H4('Team Salary Cap divided by salaries of players + additional cap space for next year'),
    dcc.Graph(id='graph'),
    html.P("Team:"),
    dcc.Dropdown(id='teams',
        options=[{'label': i, 'value': i} for i in teams],
        value='Atlanta Dream', clearable=False
    ),
    html.P("Year:"),
    dcc.Dropdown(id='year',
        options=[
                     {'label': '2023', 'value': '2023'},
                     {'label': '2024', 'value': '2024'},
                     {'label': '2025', 'value': '2025'},
                     {'label': '2026', 'value': '2026'},
                     {'label': '2027', 'value': '2027'}
            ],
        value='2023', 
        multi=False,
        clearable=False
    ),

])

#---------------------------------------------------------------
@app.callback(
    Output('graph', 'figure'),
    Input('year', 'value'),
    Input('teams', 'value')
)
def update_graph(year, team):
    dff = df[df["TEAM"] == team]
    
    fig = px.pie(dff, names = 'PLAYER', values = str(year))
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)