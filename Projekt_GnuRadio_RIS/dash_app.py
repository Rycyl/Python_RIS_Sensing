import dash
import pandas as pd
import sqlite3
from dash import Dash, html, dash_table, dcc
import plotly.express as px

conn = sqlite3.connect("temp_db.db")
curs = conn.cursor()

df = pd.read_sql_query("SELECT * FROM power_readings", conn)

app = Dash()


app.layout = [
    html.Div(children='Power readings'),
    dash_table.DataTable(
        
]

