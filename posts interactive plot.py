import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import os.path
import numpy as np
from datetime import datetime
import dateutil

sf_users = pd.read_csv(os.path.join("data","scifi.stackexchange.com", "Users.csv"))
sf_posts = pd.read_csv(os.path.join("data","scifi.stackexchange.com", "Posts.csv"))
m_users = pd.read_csv(os.path.join("data","movies.stackexchange.com", "Users.csv"))
m_posts = pd.read_csv(os.path.join("data","movies.stackexchange.com", "Posts.csv"))
w_users = pd.read_csv(os.path.join("data","writers.stackexchange.com", "Users.csv"))
w_posts = pd.read_csv(os.path.join("data","writers.stackexchange.com", "Posts.csv"))

# So what is reputation?

# Reputation is a rough measurement of how much the community trusts you;
# it is earned by convincing your peers that you know what you’re talking about. 

# posts.OwnerUserId odnosi się do users.Id (nie: users.AccountId)

sf_posts.loc[:,"Year"] = [datetime.strptime(x[0:10], '%Y-%m-%d').year
                                  for x in sf_posts.loc[:,"CreationDate"]]

w_posts.loc[:,"Year"] = [datetime.strptime(x[0:10], '%Y-%m-%d').year
                                  for x in w_posts.loc[:,"CreationDate"]]

m_posts.loc[:,"Year"] = [datetime.strptime(x[0:10], '%Y-%m-%d').year
                                  for x in m_posts.loc[:,"CreationDate"]]

# scifi
sf_df = sf_posts.loc[:,["Id", "Year", "FavoriteCount", "OwnerUserId", "PostTypeId", 
                "Score", "Title", "ViewCount"]].merge(sf_users.loc[:, ["Id", "Reputation", "Views"]],
                                                     left_on="OwnerUserId", right_on="Id")
sf_df["Source"] = "scifi" 

# movies
m_df = m_posts.loc[:,["Id", "Year", "FavoriteCount", "OwnerUserId", "PostTypeId", 
                "Score", "Title", "ViewCount"]].merge(m_users.loc[:, ["Id", "Reputation", "Views"]],
                                                     left_on="OwnerUserId", right_on="Id")
m_df["Source"] = "movies" 

# writers
w_df = w_posts.loc[:,["Id", "Year", "FavoriteCount", "OwnerUserId", "PostTypeId", 
                "Score", "Title", "ViewCount"]].merge(w_users.loc[:, ["Id", "Reputation", "Views"]],
                                                     left_on="OwnerUserId", right_on="Id")
w_df["Source"] = "writers" 

# all together
df = sf_df.append(m_df, sort=False).append(w_df, sort=False).reset_index(drop=True)
# df = df.iloc[[1,2,3,-1], :] # do przetestowania czy działa

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['Source'] == i]['Score'],
                    y=df[df['Source'] == i]['Reputation'],
                    text=df[df['Source'] == i]['Title'],
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
                xaxis={'type': 'log', 'title': 'Post Score'},
                yaxis={'title': 'User Reputation'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    #    app.run_server(debug=True)
    app.server.run()



