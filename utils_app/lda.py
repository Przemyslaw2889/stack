import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
import pandas as pd
import os
import pickle


lda_path = os.path.join("preprocessed_data", "lda")
model_path = os.path.join(lda_path, "lda_3components.pkl")


def _get_posts(colnames=None):
    colnames = colnames or ["Body", "topic"]
    # engine="python": https://github.com/pandas-dev/pandas/issues/11166
    posts_scifi = pd.read_csv(os.path.join(lda_path, "posts_topics_scifi.csv"), engine="python")
    return posts_scifi.loc[:, colnames]


def _get_lda_and_cv():
    """Returns lda model object and cv object (see lda_topic_modelling.ipynb)"""
    with open(model_path, 'rb') as f:
        lda, cv = pickle.load(f)
    return lda, cv


def _print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = 'Topic #%d: ' % topic_idx
        message += ' '.join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message + "\n")
    print()

def _get_top_words(model, feature_names, n_top_words):
    topic_words = [[], [], []]
    for topic_idx, topic in enumerate(model.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
        topic_words[topic_idx].extend(top_words)
    return topic_words


def get_top_words(n_top_words):
    lda, cv = _get_lda_and_cv()
    topic_words = _get_top_words(lda, cv.get_feature_names(), n_top_words)
    df = pd.DataFrame(list(zip(*topic_words)), columns=["topic 1", "topic 2", "topic 3"])
    return df


posts_topics = _get_posts()
max_post_length = 75
posts_topics.Body = posts_topics.Body.str.slice(0, max_post_length)


def get_topic_layout():
    img_src = 'https://miro.medium.com/max/882/1*pZo_IcxW1GVuH2vQKdoIMQ.jpeg'
    top_words = get_top_words(50)

    layout = html.Div([
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="six columns",
                    children=[
                        html.Div(
                            children=dt.DataTable(
                            data=posts_topics.to_dict('rows'),
                            columns=[{'id': c, 'name': c} for c in posts_topics.columns],
                            style_table={'overflowX': 'scroll'}
                                )
                            )
                    ]
                ),
                html.Div(
                    className="six columns",
                    children=html.Div([
                        html.Img(id='image',
                                    src=img_src),
                        dt.DataTable(
                            data=top_words.to_dict('rows'),
                            columns=[{'id': c, 'name': c} for c in top_words.columns],
                            style_table={'overflowX': 'scroll'}
                                )
                    ])
                )
            ]
        )
    ])
    return layout

