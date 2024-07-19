import dash
import pandas as pd
import sqlite3
from dash import Dash, html, dash_table, dcc
import plotly.express as px

conn = sqlite3.connect("/home/kiril/Documents/GitHub/Python_RIS_Sensing/Projekt_GnuRadio_RIS/temp_db.db")
curs = conn.cursor()

power_readings = pd.read_sql_query("SELECT * FROM power_readings", conn)

app = Dash()
print(power_readings)

app.layout = [
    html.Div(children='Power readings'),
    dash_table.DataTable(data = power_readings.to_dict('records'), page_size=10)
]

if __name__ == '__main__':
    app.run_server(debug=True)

