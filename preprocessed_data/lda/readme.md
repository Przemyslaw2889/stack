In lda_3components there is lda model (lda) and count vectorizer (cv) saved (see lda_topic_modelling.ipynb).

To restore it use:

```
with open('objs.pkl', 'rb') as f:
    lda, cv = pickle.load(f)
```
