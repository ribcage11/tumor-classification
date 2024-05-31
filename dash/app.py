# IMPORTS
import os.path
import sys

import dash_daq as daq
import plotly.express as px
import pandas as pd

from dash import Dash, html, dcc, callback, Output, Input

# Fix syspath for module import
wdir = os.getcwd() # working directory
sys.path.append(wdir)
import src.make_df as make_df
import src.DataFrameProcessor as DFP

from src.file_traversal import read_config


# CODE

# read config
config = read_config()
port_num = config["port"]

# dataframes
labels = pd.read_csv(config["labels_path"])
labels = make_df.fill_labels_df(labels)
scan_paths = make_df.fill_scan_df(labels, config)


app = Dash()
app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    html.Div([
        html.H3(children='Label distribution'),
        # Class distribution
        dcc.Graph(figure=px.bar(labels.MGMT_value.value_counts(), color=[0, 1]).update_yaxes(title_text='Frequency')),
    ]),
    # Make histogram of number of scans per patient
    html.Div([
        html.Div(
            daq.BooleanSwitch(id='label-on', on=False, labelPosition='top', label='See labels'),
            style={'display': 'inline-block', 'height': '70px', 'width': '50px'},
        ),
        dcc.Graph(id='scans-distribution'),
        dcc.Slider(id='bin-slider', min=3, max=9, step=2, marks={i: f'{i}' for i in [3, 5, 9]}, value=9),
    ])
]


# Make histogram of number of scans per patient
@callback(
    Output('scans-distribution', 'figure'),
    Input('label-on', 'on'),
    Input('bin-slider', 'value')
)
def scan_distribution_data(show_labels, bins):
    im_counts = scan_paths.BraTS21ID.value_counts()  # count number of scans in patient dir
    if show_labels:
        im_counts = pd.merge(im_counts, labels, left_index=True, right_on='BraTS21ID')
        fig = px.histogram(im_counts, x='count', nbins=bins, color="MGMT_value")
    else:
        fig = px.histogram(im_counts, x='count', nbins=bins)
    fig.update_xaxes(title_text='Number of scans per patient')
    fig.update_yaxes(title_text='Frequency')
    return fig


if __name__ == '__main__':
    app.run(debug=True, port=port_num)
