#!/usr/bin/python
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os
import pickle

from utils_app.get_map import get_scatter_map, get_scattermapbox, get_map_layout
from utils_app.lda import get_topic_layout
from utils_app.interactive_plot import get_interactive_graph_layout, df
from utils_app.countries_posts_interactive import get_countries_posts_layout, df_countries


### DASH APP ###

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Map', value='tab_map',
                children = get_map_layout()),
        dcc.Tab(label='Topic modelling', value='tab_topics',
                children = get_topic_layout()),
        dcc.Tab(label='Users posts and reputation', value='tab_graph',
                children = get_interactive_graph_layout()),
        dcc.Tab(label='Changes in time', value='tab_countries',
                children = get_countries_posts_layout())
    ]),
    html.Div(id='tabs-content'),
])


@app.callback(
    Output('posts_inter', 'figure'),
    [Input('ques_ans', 'value'),
     Input('year_slider', 'value')])
def update_graph(post_type, year_value):
    dff = df[(df.Year.between(year_value[0], year_value[1])) & (df.PostTypeId == post_type)]
    return {
        'data': [
            go.Scatter(
                x=dff[dff['Source'] == i]['Reputation'],
                y=dff[dff['Source'] == i]['Score'],
                text=dff[dff['Source'] == i]['Title'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in df.Source.unique()
        ],
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'User Reputation'},
            yaxis={'title': 'Post Score'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


@app.callback(
    dash.dependencies.Output('countries_inter', 'figure'),
    [dash.dependencies.Input('source_dropdown', 'value'),
    dash.dependencies.Input('year_slider_countries', 'value')])
def update_graph_countries(source_value, year_value):
    dff = df_countries[(df_countries.Source == source_value) & (df_countries.Year == year_value)]
    return {
        'data': [
            go.Scatter(
                x=dff[dff['continent'] == i]['UsersCount'],
                y=dff[dff['continent'] == i]['PostsCount'],
                text=dff[dff['continent'] == i]['country'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in df_countries['continent'].unique()
        ],
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'Number of Users'},
            yaxis={'title': 'Number of Posts'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)