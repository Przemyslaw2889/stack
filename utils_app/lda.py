import pandas as pd
import os
import pickle


lda_path = os.path.join("preprocessed_data", "lda")
model_path = os.path.join(lda_path, "lda_3components.pkl")

def get_posts(colnames=None):
    colnames = ["Body", "topic"]
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

def print_topic_words(n_top_words):
    lda, cv = _get_lda_and_cv()
    _print_top_words(lda, cv, n_top_words)
