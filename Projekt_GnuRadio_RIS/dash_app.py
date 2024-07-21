#import dash
import pandas as pd
import sqlite3
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import os

conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_db.db'))   #("/home/kiril/Documents/GitHub/Python_RIS_Sensing/Projekt_GnuRadio_RIS/temp_db.db")
curs = conn.cursor()

power_readings_full = pd.read_sql_query("SELECT * FROM power_readings", conn)

crit_1 = (power_readings_full['RIS_connected'] == 'No')

power_readings = power_readings_full[~crit_1]

app = Dash()
#print(power_readings)

app.layout = [
    html.Div(children='Power readings'),
    html.Hr(),
    dcc.RadioItems(options=['power', 'timestamp', 'params_id'], value='params_id', id='controls-and-radio-item'),
    dash_table.DataTable(data = power_readings.to_dict('records'), page_size=10),
    dcc.Graph(figure={}, id='controls-and-graph')
]

@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graps(col_chosen):
    fig = px.histogram(power_readings, x='RIS_1_pattern', y=col_chosen, histfunc='avg')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

