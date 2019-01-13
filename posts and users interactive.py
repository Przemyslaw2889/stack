import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import os.path
import numpy as np
from datetime import datetime
import dateutil
import  lxml

sf_users = pd.read_csv(os.path.join("preprocessed_data", "users_scifi_location.csv"))
w_users = pd.read_csv(os.path.join("preprocessed_data", "users_writers_location.csv"))
m_users = pd.read_csv(os.path.join("preprocessed_data", "users_movies_location.csv"))
sf_posts = pd.read_csv(os.path.join("data","movies.stackexchange.com", "Posts.csv"))
w_posts = pd.read_csv(os.path.join("data","writers.stackexchange.com", "Posts.csv"))
m_posts = pd.read_csv(os.path.join("data","writers.stackexchange.com", "Posts.csv"))

adres = "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"
res = pd.read_html(adres)
continents = res[1]
continents.columns = ["id", "country", "continent", "region","a","b","c"]

sf_users = sf_users.merge(continents[["country", "continent"]], on = "country")
w_users = w_users.merge(continents[["country", "continent"]], on = "country")
m_users = m_users.merge(continents[["country", "continent"]], on = "country")

continents["country"] = [i.split("[")[0] for i in continents.country]
continents[["country", "continent"]].head()

sf_posts.loc[:,"Year"] = [datetime.strptime(x[0:10], '%Y-%m-%d').year
                                  for x in sf_posts.loc[:,"CreationDate"]]

w_posts.loc[:,"Year"] = [datetime.strptime(x[0:10], '%Y-%m-%d').year
                                  for x in w_posts.loc[:,"CreationDate"]]

m_posts.loc[:,"Year"] = [datetime.strptime(x[0:10], '%Y-%m-%d').year
                                  for x in m_posts.loc[:,"CreationDate"]]

sf_users.loc[:,"Year"] = [datetime.strptime(x[0:10], '%Y-%m-%d').year
                                  for x in sf_users.loc[:,"CreationDate"]]

w_users.loc[:,"Year"] = [datetime.strptime(x[0:10], '%Y-%m-%d').year
                                  for x in w_users.loc[:,"CreationDate"]]

m_users.loc[:,"Year"] = [datetime.strptime(x[0:10], '%Y-%m-%d').year
                                  for x in m_users.loc[:,"CreationDate"]]

sf_posts = sf_posts.merge(sf_users[["Id", "country", "continent"]], left_on = "OwnerUserId", right_on="Id")
w_posts = w_posts.merge(w_users[["Id", "country", "continent"]], left_on = "OwnerUserId", right_on="Id")
m_posts = m_posts.merge(m_users[["Id", "country", "continent"]], left_on = "OwnerUserId", right_on="Id")

sf_posts_in_time = sf_posts.groupby(["Year", "country", "continent"]).size().rename("PostsCount").reset_index()
sf_posts_in_time["Source"] = "scifi"

w_posts_in_time = w_posts.groupby(["Year", "country", "continent"]).size().rename("PostsCount").reset_index()
w_posts_in_time["Source"] = "writers"

m_posts_in_time = m_posts.groupby(["Year", "country", "continent"]).size().rename("PostsCount").reset_index()
m_posts_in_time["Source"] = "movies"

sf_users_in_time = sf_users.groupby(["Year", "country", "continent"]).size().rename("UsersCount").reset_index()
# sf_users_in_time = sf_users_in_time[:-1]

w_users_in_time = w_users.groupby(["Year", "country", "continent"]).size().rename("UsersCount").reset_index()
# w_users_in_time = w_users_in_time[:-1]

m_users_in_time = m_users.groupby(["Year", "country", "continent"]).size().rename("UsersCount").reset_index()
# m_users_in_time = m_users_in_time[:-1]   

sf_df = sf_users_in_time.merge(sf_posts_in_time, on = ["Year", "country", "continent"])
w_df = w_users_in_time.merge(w_posts_in_time, on = ["Year", "country", "continent"])
m_df = m_users_in_time.merge(m_posts_in_time, on = ["Year", "country", "continent"])

df = sf_df.append(w_df, sort=False).append(m_df, sort=False).reset_index(drop=True)

YEARS = df.Year.unique()

# ---------

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([

    html.H4('How does "stackexchange" popularity changed in time?'),
    html.Div(dcc.Graph(id='posts_inter')),
    html.Div([
        html.Label('Year'),
        dcc.Slider(
            id = "year_slider",
            min=min(YEARS),
            max=max(YEARS),
            value=min(YEARS),
            marks={str(year): str(year) for year in YEARS}
            )]),
    html.Div([
        html.Label('stackexchange'),
        dcc.Dropdown(
            id='source_dropdown',
            options=[{'label': i, 'value': i} for i in df.Source.unique()],
            #options=[{'label': i, 'value': i} for i in available_indicators],
            value=df.Source.unique()[0]
            )])

])

@app.callback(
    dash.dependencies.Output('posts_inter', 'figure'),
    [dash.dependencies.Input('source_dropdown', 'value'),
    dash.dependencies.Input('year_slider', 'value')])
def update_graph(source_value, year_value):
    dff = df[(df.Source == source_value) & (df.Year == year_value)]
    return {
        'data': [
            go.Scatter(
                x=dff[dff.continent == i]['UsersCount'],
                y=dff[dff['continent'] == i]['PostsCount'],
                text=dff[dff['continent'] == i]['country'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in df.continent.unique()
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
    app.server.run()