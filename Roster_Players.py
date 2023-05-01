import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.dash_table import DataTable


teams = ['Atlanta Dream.csv', 'Chicago Sky.csv', 'Connecticut Sun.csv', 'Dallas Wings.csv', 'Indiana Fever.csv', 'Las Vegas Aces.csv', 'Los Angeles Sparks.csv', 'Minnesota Lynx.csv', 'New York Liberty.csv', 'Phoenix Mercury.csv', 'Seattle Storm.csv', 'Washington Mystics.csv']


teams_columns = ['PLAYER', '2023 TYPE', '2023', '2024 TYPE', '2024', '2025 TYPE', '2025', '2026 TYPE', '2026', '2027 TYPE', '2027', 'CORE YEARS']

teams_dict = {'Atlanta Dream':'Atlanta Dream.csv', 'Chicago Sky':'Chicago Sky.csv', 'Connecticut Sun':'Connecticut Sun.csv', 'Dallas Wings':'Dallas Wings.csv', 'Indiana Fever':'Indiana Fever.csv', 'Las Vegas Aces':'Las Vegas Aces.csv', 'Los Angeles Sparks':'Los Angeles Sparks.csv', 'Minnesota Lynx':'Minnesota Lynx.csv', 'New York Liberty':'New York Liberty.csv', 'Phoenix Mercury':'Phoenix Mercury.csv', 'Seattle Storm':'Seattle Storm.csv', 'Washington Mystics':'Washington Mystics.csv'   
 }


df1 = pd.read_csv(teams_dict['Atlanta Dream'], usecols=teams_columns)
df2 = pd.read_csv(teams_dict['Chicago Sky'], usecols=teams_columns)
df3 = pd.read_csv(teams_dict['Connecticut Sun'], usecols=teams_columns)
df4 = pd.read_csv(teams_dict['Dallas Wings'], usecols=teams_columns)
df5 = pd.read_csv(teams_dict['Indiana Fever'], usecols=teams_columns)
df6 = pd.read_csv(teams_dict['Las Vegas Aces'], usecols=teams_columns)
df7 = pd.read_csv(teams_dict['Los Angeles Sparks'], usecols=teams_columns)
df8 = pd.read_csv(teams_dict['Minnesota Lynx'], usecols=teams_columns)
df9 = pd.read_csv(teams_dict['New York Liberty'], usecols=teams_columns)
df10 = pd.read_csv(teams_dict['Phoenix Mercury'], usecols=teams_columns)
df11 = pd.read_csv(teams_dict['Seattle Storm'], usecols=teams_columns)
df12 = pd.read_csv(teams_dict['Washington Mystics'], usecols=teams_columns)


df_list = [(df1, 'Atlanta Dream'), (df2, 'Chicago Sky'), (df3, 'Connecticut Sun'), (df4, 'Dallas Wings'), (df5, 'Indiana Fever'), (df6, 'Las Vegas Aces'), (df7, 'Los Angeles Sparks'), (df8, 'Minnesota Lynx'), (df9, 'New York Liberty'), (df10, 'Phoenix Mercury'), (df11, 'Seattle Storm'), (df12, 'Washington Mystics')]

 # merge the dataframes using pd.concat(), adding a new column indicating the source dataframe
merged_df = pd.concat([df.assign(source=source) for df, source in df_list], ignore_index=True)

 # move the source column to the front of the dataframe
merged_df.insert(0, 'TEAM', merged_df.pop('source'))
merged_df.fillna(value= "--", inplace=True)
pattern = r'Total|Roster|Veteran|Roster|Player|Cap Room|Salary|Minimum|--|2023|2024|2025'
mask = ~merged_df['PLAYER'].str.contains(pattern)
merged_df = merged_df[mask]

merged_df['2023 TYPE'] = merged_df['2023 TYPE'].replace({'V': 'Protected Veteran', 'R': 'Protected Rookie Scale', 'U': 'Unprotected', 
                                               'OPT': 'Team Option', 'TC': 'Training Camp', 
                                               'D': 'Draftee', 'Reserved': 'Reserved Free Agent',
                                              'SuspCE': 'Suspended-Contract Expired'})

merged_df['2024 TYPE'] = merged_df['2024 TYPE'].replace({'V': 'Protected Veteran', 'R': 'Protected Rookie Scale', 'U': 'Unprotected', 
                                               'OPT': 'Team Option', 'TC': 'Training Camp', 
                                               'D': 'Draftee', 'Reserved': 'Reserved Free Agent',
                                              'SuspCE': 'Suspended-Contract Expired'})

merged_df['2025 TYPE'] = merged_df['2025 TYPE'].replace({'V': 'Protected Veteran', 'R': 'Protected Rookie Scale', 'U': 'Unprotected', 
                                               'OPT': 'Team Option', 'TC': 'Training Camp', 
                                               'D': 'Draftee', 'Reserved': 'Reserved Free Agent',
                                              'SuspCE': 'Suspended-Contract Expired'})

merged_df['2026 TYPE'] = merged_df['2025 TYPE'].replace({'V': 'Protected Veteran', 'R': 'Protected Rookie Scale', 'U': 'Unprotected', 
                                               'OPT': 'Team Option', 'TC': 'Training Camp', 
                                               'D': 'Draftee', 'Reserved': 'Reserved Free Agent',
                                              'SuspCE': 'Suspended-Contract Expired'})

merged_df['2027 TYPE'] = merged_df['2025 TYPE'].replace({'V': 'Protected Veteran', 'R': 'Protected Rookie Scale', 'U': 'Unprotected', 
                                               'OPT': 'Team Option', 'TC': 'Training Camp', 
                                               'D': 'Draftee', 'Reserved': 'Reserved Free Agent',
                                              'SuspCE': 'Suspended-Contract Expired'})

options = [{'label': val, 'value': val} for val in merged_df['TEAM'].unique()]

color_scale = [    {'if': {'column_id': '2023 TYPE', 'filter_query': '{2023 TYPE} eq "UFA"'}, 'backgroundColor': 'blue', 'color': 'white'},     {'if': {'column_id': '2024 TYPE', 'filter_query': '{2024 TYPE} eq "UFA"'}, 'backgroundColor': 'blue', 'color': 'white'},    {'if': {'column_id': '2025 TYPE', 'filter_query': '{2025 TYPE} eq "UFA"'}, 'backgroundColor': 'blue', 'color': 'white'},     {'if': {'column_id': '2026 TYPE', 'filter_query': '{2026 TYPE} eq "UFA"'}, 'backgroundColor': 'blue', 'color': 'white'},    {'if': {'column_id': '2027 TYPE', 'filter_query': '{2027 TYPE} eq "UFA"'}, 'backgroundColor': 'blue', 'color': 'white'}]


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Current Roster Players' Salaries"),
    dcc.Dropdown(
        id='dropdown',
        options=options,
        value=options[0]['value']
    ),
    DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in merged_df.columns],
        data=merged_df.to_dict('records'),
        style_data_conditional=color_scale
    )
])

@app.callback(Output('table', 'data'),
              [Input('dropdown', 'value')])
def update_table(value):
    filtered_df = merged_df[merged_df['TEAM'] == value]
    return filtered_df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)