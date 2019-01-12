"""Plotting map"""
import pandas as pd
import numpy as np
import plotly
import plotly.plotly as py
import os

users_scifi = pd.read_csv(os.path.join("preprocessed_data", "users_scifi_location.csv"))

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
            colorbar = dict(
                autotick = False,
                tickprefix = '$',
                title = 'GDP<br>Billions US$'),
        ) ]

    layout = dict(
        title = 'Mapa',
        geo = dict(
            showframe = False,
            showcoastlines = False,
            projection = dict(
                type = 'Mercator'
            )
        )
    )

    fig = dict(data=data, layout=layout)
    return py.iplot(fig, validate=False, filename='d3-world-map' )


