# IMPORTS
import os.path
import sys

import dash_daq as daq
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, html, dcc, callback, Output, Input

# Fix syspath for module import
wdir = os.getcwd()  # working directory
sys.path.append(wdir)
import src.make_df as make_df
import src.process_data as proc_data

from src.file_traversal import read_config

# CODE

# Config
config = read_config()
port_num = config['port']

# Dataframes
labels = pd.read_csv(config['labels_path'])
labels = make_df.fill_labels_df(labels)
scan_paths = make_df.fill_scan_df(labels, config)


# Layout
app = Dash()
app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            html.H3(children='Label distribution'),
            # Class distribution
            dcc.Graph(figure=px.bar(labels.MGMT_value.value_counts(), color=[0, 1]).update_yaxes(title_text='Frequency')),
        ], style={'display': 'inline-block', 'width': '50%'},),
        # Make histogram of number of scans per patient
        html.Div([
            html.Div(
                daq.BooleanSwitch(id='label-on', on=False, labelPosition='top', label='See labels'),
                style={'display': 'inline-block', 'height': '70px', 'width': '60px'},
            ),
            dcc.Graph(id='scans-distribution'),
            dcc.Slider(id='bin-slider', min=3, max=9, step=2, marks={i: f'{i}' for i in [3, 5, 9]}, value=9),
        ], style={'display': 'inline-block', 'width': '50%'}),
    ]),
    html.Div([
        html.Div([
            html.H3(children='Scan Preview'),
            dcc.Input(value='00000', id='pid-textbox'),
            dcc.Graph(id='3d-scan'),
        ]),
        html.Div([
            html.H3(children='Variance per cross-section'),
            dcc.Graph(id='var-dist'),
        ]),
    ]),
    html.Div([

    ])

]


# Callbacks
# Make histogram of number of scans per patient
@callback(
    Output('scans-distribution', 'figure'),
    Input('label-on', 'on'),
    Input('bin-slider', 'value')
)
def scan_distribution_data(show_labels, bins):
    im_counts = scan_paths.pid.value_counts()  # count number of scans in patient dir
    if show_labels:
        im_counts = pd.merge(im_counts, labels, left_index=True, right_on='pid')
        fig = px.histogram(im_counts, x='count', nbins=bins, color='MGMT_value')
    else:
        fig = px.histogram(im_counts, x='count', nbins=bins)
    fig.update_xaxes(title_text='Number of scans per patient')
    fig.update_yaxes(title_text='Frequency')
    return fig


@callback(
    Output('3d-scan', 'figure'),
    Output('var-dist', 'figure'),
    Input('pid-textbox', 'value')
)
def view_3d_scan(pid):
    patient = proc_data.read_full_3d_scan(scan_paths, pid)
    scan = px.imshow(patient, animation_frame=0, binary_string=True)

    var = (patient/patient.max()).var(dim=['x', 'y'])  # Compute max_scaled variance
    var = pd.Series(var)  # Store in pd.Series for quick plotting
    var_plot = px.line(var)
    var_plot.update_xaxes(title_text='Image index')
    var_plot.update_yaxes(title_text='Variance')
    return scan, var_plot


if __name__ == '__main__':
    app.run(debug=True, port=port_num)
