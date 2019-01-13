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

#df = df.loc[(df.Score == df.Score) & (df.FavoriteCount==df.FavoriteCount),:].reset_index(drop=True)
df = df.iloc[(range(1000, 200000, 200)),:] # do przetestowania czy działa

YEARS = df.Year.unique()
#YEARS = [int(year) for year in YEARS]

available_indicators = pd.DataFrame({'TypeId':[1,2,3,4,5,6,7,8],\
'PostType':["Question", "Answer", "Orphaned tag wiki", "Tag wiki excerpt",\
"Tag wiki", "Moderator nomination", "Wiki placeholder","Privilege wiki"]})

# available_indicators = ["Question", "Answer", "Orphaned tag wiki", "Tag wiki excerpt",\
# "Tag wiki", "Moderator nomination", "Wiki placeholder","Privilege wiki"]

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def get_interactive_graph_layout():

    layout = html.Div([

        html.H4('Does experience help you write better posts?'),
        html.Div(dcc.Graph(id='posts_inter')),
        html.Div([
            html.Label('Type of Post'),
            dcc.Dropdown(
                    id='ques_ans',
                    options=[{'label': available_indicators.iloc[i,1], 'value': available_indicators.iloc[i,0]} for i in range(0,8)],
                    #options=[{'label': i, 'value': i} for i in available_indicators],
                    value=available_indicators.iloc[0,0]
                )]),
        html.Div([
            html.Label('Post Creation Date'),
            dcc.RangeSlider(
            id = "year_slider",
            min=min(YEARS),
            max=max(YEARS),
            value=[min(YEARS), max(YEARS)],
            marks={str(year): str(year) for year in YEARS}
            )])

    ])
    return layout


if __name__ == '__main__':
    #    app.run_server(debug=True)
    app.server.run()



