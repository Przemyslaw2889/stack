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

from utils_app.get_map import get_map
from utils_app.lda import get_posts


# Preparing data
users_scifi = pd.read_csv(os.path.join("preprocessed_data", "users_scifi_location.csv"))
posts_topics = get_posts()
posts_topics.Body = posts_topics.Body.str.slice(0, 75)

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
        dcc.Tab(label='Map', value='tab_map'),
        dcc.Tab(label='Topic modelling', value='tab_topics'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab_map':
        data, layout = get_map()
        return dcc.Graph(
            figure=go.Figure(
                data=data,
                layout=layout
            ),
            style={'height': 500, 'width':1300},
            id='world_map'
        )

    elif tab == 'tab_topics':
        return html.Div(
                        [
                        html.Div(
                                [
                                dt.DataTable(
                                data=posts_topics.to_dict('rows'),
                                columns=[{'id': c, 'name': c} for c in posts_topics.columns],
                                style_table={'overflowX': 'scroll'}
                                )
                                ],
                                style={'width':'50%',
                                        'maxHeight': '500',
                                        'overflowY': 'scroll'
                                        },
                            ),
                        html.Div(
                            [
                                html.H1("Hello")
                            ],
                        )
                    ]
                )
                
if __name__ == '__main__':
    app.run_server(debug=True)