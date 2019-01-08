import pandas as pd
import numpy as np
import os.path
from datetime import datetime

from bokeh.layouts import row, widgetbox
from bokeh.models import Select
from bokeh.palettes import Spectral5
from bokeh.plotting import curdoc, figure
from bokeh.io import output_file, show

users = pd.read_csv(os.path.join("data","scifi.stackexchange.com", "Users.csv"))
posts = pd.read_csv(os.path.join("data","scifi.stackexchange.com", "Posts.csv"))
comments = pd.read_csv(os.path.join("data","scifi.stackexchange.com", "Comments.csv"))

users.loc[:,"CreationDate"] = [datetime.strptime(x[0:10], '%Y-%m-%d').strftime('%Y-%m')
                                  for x in users.loc[:,"CreationDate"]]

posts.loc[:,"CreationDate"] = [datetime.strptime(x[0:10], '%Y-%m-%d').strftime('%Y-%m')
                                  for x in posts.loc[:,"CreationDate"]]

comments.loc[:,"CreationDate"] = [datetime.strptime(x[0:10], '%Y-%m-%d').strftime('%Y-%m')
                                  for x in comments.loc[:,"CreationDate"]]

posts_in_time = posts.groupby("CreationDate").size()\
.rename("no_posts").to_frame()
posts_in_time = posts_in_time[:-1]

users_in_time = users.groupby("CreationDate").size()\
.rename("no_users").to_frame()
users_in_time = users_in_time[:-1]

comments_in_time = comments.groupby("CreationDate").size()\
.rename("no_comments").to_frame()
comments_in_time = comments_in_time[:-1]

total_users_in_time = users.groupby("CreationDate").size().cumsum()\
.rename("total_users").to_frame()
total_users_in_time = total_users_in_time[:-1]

questions_in_time = posts.query("PostTypeId == 1").groupby("CreationDate")\
.size().cumsum().rename("no_questions").to_frame()
questions_in_time = questions_in_time[:-1]

answers_in_time = posts.query("PostTypeId == 2").groupby("CreationDate")\
.size().cumsum().rename("no_answers").to_frame()
answers_in_time = answers_in_time[:-1]

df = posts_in_time.join(users_in_time, how = "outer")\
.join(comments_in_time, how = "outer")\
.join(total_users_in_time, how = "outer")\
.join(questions_in_time, how = "outer")\
.join(answers_in_time, how = "outer")\
.reset_index()

SIZES = list(range(6, 22, 3))
COLORS = Spectral5
N_SIZES = len(SIZES)
N_COLORS = len(COLORS)

columns = sorted(df.columns)

discrete = [x for x in columns if df[x].dtype == object]
continuous = [x for x in columns if x not in discrete]

def create_figure():
    xs = df[x.value].values
    ys = df[y.value].values
    x_title = x.value.title()
    y_title = y.value.title()

    kw = dict()
    if x.value in discrete:
        kw['x_range'] = sorted(set(xs))
    if y.value in discrete:
        kw['y_range'] = sorted(set(ys))
    kw['title'] = "%s vs %s" % (x_title, y_title)

    p = figure(plot_height=600, plot_width=800, tools='pan,box_zoom,hover,reset', **kw)
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    if x.value in discrete:
        p.xaxis.major_label_orientation = pd.np.pi / 4

    sz = 9
    if size.value != 'None':
        if len(set(df[size.value])) > N_SIZES:
            groups = pd.qcut(df[size.value].values, N_SIZES, duplicates='drop')
        else:
            groups = pd.Categorical(df[size.value])
        sz = [SIZES[xx] for xx in groups.codes]

    c = "#31AADE"
    if color.value != 'None':
        if len(set(df[color.value])) > N_SIZES:
            groups = pd.qcut(df[color.value].values, N_COLORS, duplicates='drop')
        else:
            groups = pd.Categorical(df[color.value])
        c = [COLORS[xx] for xx in groups.codes]

    p.circle(x=xs, y=ys, color=c, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)

    return p


def update(attr, old, new):
    layout.children[1] = create_figure()
    
# output_file("test2.html")

x = Select(title='X-Axis', value='no_users', options=columns)
x.on_change('value', update)

y = Select(title='Y-Axis', value='no_posts', options=columns)
y.on_change('value', update)

size = Select(title='Size', value='None', options=['None'] + continuous)
size.on_change('value', update)

color = Select(title='Color', value='None', options=['None'] + continuous)
color.on_change('value', update)

controls = widgetbox([x, y, color, size], width=200)
layout = row(controls, create_figure())

curdoc().add_root(layout)
curdoc().title = "Crossfilter"

show(layout)


## uruchamianie: w terminalu wpisać:
# bokeh serve --show interaction.py

# ewentualnie: bokeh serve --show --port 5001 interaction.py