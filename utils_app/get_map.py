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
    #return py.iplot(fig, validate=False, filename='d3-world-map' )


def get_scatter_map():
    scl = [0,"rgb(150,0,90)"],[0.125,"rgb(0, 0, 200)"],[0.25,"rgb(0, 25, 255)"],\
    [0.375,"rgb(0, 152, 255)"],[0.5,"rgb(44, 255, 150)"],[0.625,"rgb(151, 255, 0)"],\
    [0.75,"rgb(255, 234, 0)"],[0.875,"rgb(255, 111, 0)"],[1,"rgb(255, 0, 0)"]

    df = users_scifi.sort_values("Reputation", ascending=True)

    data = [ dict(
        lat = df['lat'],
        lon = df['lon'],
        text = df['DisplayName'].astype(str) + ' ' + df['Reputation'].astype(str),
        marker = dict(
            color = df['Reputation'],
            colorscale = scl,
            reversescale = True,
            opacity = 0.7,
            size = 2,
            colorbar = dict(
                title='reputation'
            ),
        ),
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
            lakecolor = "rgb(0, 191, 255)",
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