"""Plotting map"""
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import plotly
import plotly.plotly as py
import os
import matplotlib. pyplot as plt
from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap

users_scifi = pd.read_csv(os.path.join("preprocessed_data", "users_scifi_location.csv"))


def get_map_layout():
    data, layout = get_scattermapbox()
    return dcc.Graph(
        figure=go.Figure(
            data=data,
            layout=layout
        ),
        style={'height': 500, 'width':1300},
        id='world_map'
    )


def get_scattermapbox():
# https://gist.github.com/chriddyp/1a95f6582a5256db9847086232987bff The best example I've found

    scl = [0,"rgb(150,0,90)"],[0.125,"rgb(0, 0, 200)"],[0.25,"rgb(0, 25, 255)"],\
        [0.375,"rgb(0, 152, 255)"],[0.5,"rgb(44, 255, 150)"],[0.625,"rgb(151, 255, 0)"],\
        [0.75,"rgb(255, 234, 0)"],[0.875,"rgb(255, 111, 0)"],[1,"rgb(255, 0, 0)"]

    def get_size(reputation):
        if reputation < 10:
            return 3
        elif reputation < 100:
            return 4
        elif reputation < 1000:
            return 5
        elif reputation < 10_000:
            return 6
        else:
            return 8

    df = users_scifi.sort_values("Reputation", ascending=True)
    df = df.groupby(['lat', 'lon']).first().reset_index()

    data = [{
        'lat': df['lat'],
        'lon': df['lon'],
        'marker': {
            'color': df['Reputation'],
            'size': [get_size(reputation) for reputation in df['Reputation']],
            'opacity': 1,
            'colorscale': scl,
            'reversescale': False,
            'cmax': df['Reputation'].max(),
            'colorbar': dict(
                title="Users Reputation"
            )
        },
        'text': df['DisplayName'].astype(str) + ', ' + df['Reputation'].astype(str),
        # 'customdata': df['storenum'],
        'type': 'scattermapbox'
    }]
    layout = {
        'mapbox': {
            'accesstoken': 'pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2ozcGI1MTZ3MDBpcTJ3cXR4b3owdDQwaCJ9.8jpMunbKjdq1anXwU5gxIw'
        },
        'hovermode': 'closest',
        'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0}
    }

    return data, layout


def get_map():
    with open('api_key.txt') as f:
        line = f.readline()
        api_key = line.strip()

    countries_codes = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')
    users = pd.merge(users_scifi, countries_codes.loc[:,["COUNTRY", "CODE"]], 
                     left_on="country", right_on="COUNTRY", how="left")

    users_grouped = users.groupby(["COUNTRY", "CODE"]).size().reset_index()
    users_grouped.columns = ["country", "code", "count"]

    plotly.tools.set_credentials_file(username='kaletap', api_key=api_key)

    df = users_grouped

    data = [ dict(
            type = 'choropleth',
            locations = df['code'],
            z = df['count'],
            text = df['country'],
            colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
                [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
            autocolorscale = False,
            reversescale = True,
            marker = dict(
                line = dict (
                    color = 'rgb(180,180,180)',
                    width = 0.5
                ) ),
        ) ]

    layout = dict(
        title = 'Mapa',
        geo = dict(
            showframe = False,
            showcoastlines = False,
            projection = dict(
                type = 'mercator'
            )
        )
    )

    return data, layout


def get_scatter_map():

    df = users_scifi.sort_values("Reputation", ascending=True)
    df = df.groupby(['lat', 'lon']).first().reset_index()

    scl = [0,"rgb(150,0,90)"],[0.125,"rgb(0, 0, 200)"],[0.25,"rgb(0, 25, 255)"],\
        [0.375,"rgb(0, 152, 255)"],[0.5,"rgb(44, 255, 150)"],[0.625,"rgb(151, 255, 0)"],\
        [0.75,"rgb(255, 234, 0)"],[0.875,"rgb(255, 111, 0)"],[1,"rgb(255, 0, 0)"]

    data = [ dict(
        lat = df['lat'],
        lon = df['lon'],
        text = df['DisplayName'].astype(str) + ', ' + df['Reputation'].astype(str),
        marker =  {
                'color': df['Reputation'],
                'size': 8,
                'opacity': 0.6
            },
        type = 'scattergeo'
    ) ]

    layout = dict(
        geo = dict(
            scope = 'world',
            showland = True,
            landcolor = "rgb(212, 212, 212)",
            subunitcolor = "rgb(255, 255, 255)",
            countrycolor = "rgb(255, 255, 255)",
            showlakes = True,
            lakecolor = "rgb(255, 255, 255)",
            showsubunits = True,
            showcountries = True,
            resolution = 50,
            # projection = dict(
            #     type = 'conic conformal',
            #     rotation = dict(
            #         lon = -100
            #     )
            # ),
            # lonaxis = dict(
            #     showgrid = True,
            #     gridwidth = 0.5,
            #     range= [ -140.0, -55.0 ],
            #     dtick = 5
            # ),
            # lataxis = dict (
            #     showgrid = True,
            #     gridwidth = 0.5,
            #     range= [ 20.0, 60.0 ],
            #     dtick = 5
            # )
        ),
        title = 'Users of scifi forum',
    )
    fig = { 'data':data, 'layout':layout }
    return data, layout
