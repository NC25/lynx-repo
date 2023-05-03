import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.dash_table import DataTable


df1 = pd.read_csv('Rookie_Scale.csv')
df2 = pd.read_csv('WNBA 2023 Draft Results.csv')

df1 = df1[df1['Salary Cap Year'] == 2023]
df3 = df2.set_index('Pick').join(df1.set_index('Pick'))
df3['Team'] = df3['Team'].str.replace('*', '')
column_to_move = df3.pop('Salary Cap Year')  
df3.insert(loc=0, column='Salary Cap Year', value=column_to_move) 
df4 = pd.read_csv('Rookie_Scale.csv')
df5 = df4[df4['Salary Cap Year'] > 2023]
df_merged = pd.concat([df3, df5], ignore_index=True)
df_merged['Pick'] = df_merged['Pick'].fillna(pd.Series(range(1, 37)))
column_to_move2 = df_merged.pop('Pick')  # remove the column from the dataframe
df_merged.insert(loc=1, column='Pick', value=column_to_move2) 

options = [{'label': val, 'value': val} for val in df_merged['Salary Cap Year'].unique()]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Rookies' and Upcoming Draftees' Salaries"),
    dcc.Dropdown(
        id='dropdown',
        options=options,
        value=options[0]['value']
    ),
    DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df_merged.columns],
        data=df_merged.to_dict('records')
    )
])

@app.callback(Output('table', 'data'),
            [Input('dropdown', 'value')])

def update_table(value):
    filtered_df = df_merged[(df_merged['Salary Cap Year'] == value)]
    return filtered_df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
    

