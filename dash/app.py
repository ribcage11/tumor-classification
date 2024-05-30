# IMPORTS
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Import statements for src modules in parent directory
from inspect import getsourcefile
import os.path
import sys

# Find path operations
current_path = os.path.abspath(getsourcefile(lambda:0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir)
import src.file_traversal
from src.file_traversal import read_config


# CODE
config = read_config()
port_num = config["port"]

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash()
app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
]

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')


if __name__ == '__main__':
    app.run(debug=True, port=port_num)


