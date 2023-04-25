import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.dash_table import DataTable


df = pd.read_csv('Unsigned Draftees.csv')

options = [{'label': val, 'value': val} for val in df['TEAM'].unique()]

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=options,
        value=options[0]['value']
    ),
    DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records')
    )
])

@app.callback(Output('table', 'data'),
              [Input('dropdown', 'value')])
def update_table(value):
    filtered_df = df[df['TEAM'] == value]
    return filtered_df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)