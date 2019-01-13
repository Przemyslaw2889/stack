import dash
import dash_core_components as dcc
import dash_html_components as html
# import dash_table_experiments as dt
import dash_table as dt
from dash.dependencies import Input, Output
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os
import pickle

from utils_app.get_map import get_scatter_map, get_scattermapbox, get_map_layout
from utils_app.lda import get_topics_layout
from utils_app.interactive_plot import get_interactive_graph_layout, df


# API key
with open('api_key.txt') as f:
    line = f.readline()
    api_key = line.strip()

### DASH APP ###

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

layout_table = dict(
    autosize=True,
    # height=500,
    font=dict(color="#191A1A"),
    # titlefont=dict(color="#191A1A", size='14'),
    # margin=dict(
    #     l=35,
    #     r=35,
    #     b=35,
    #     t=45
    # ),
    # hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    # legend=dict(font=dict(size=10), orientation='h'),
)
layout_table['font-size'] = '12'
layout_table['margin-top'] = '20'



app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Map', value='tab_map',
                children = get_map_layout()),
        dcc.Tab(label='Topic modelling', value='tab_topics',
                children = get_topics_layout()),
        dcc.Tab(label='Graph', value='tab_graph',
                children = get_interactive_graph_layout())
    ]),
    html.Div(id='tabs-content'),
])

# @app.callback(Output('tabs-content', 'children'),
#               [Input('tabs', 'value'),
#                Input('ques_ans', 'value'),
#                Input('year_slider', 'value')])
# def render_content(tab, post_type, year_value):
#     if tab == 'tab_map':
#         return get_map_layout()

#     elif tab == 'tab_topics':
#         return get_topics_layout()

#     elif tab == 'tab_graph':
#         update_graph(post_type, year_value)


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


if __name__ == '__main__':
    app.run_server(debug=True)