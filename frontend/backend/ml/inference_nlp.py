import re
from string import punctuation

import nltk
import pandas as pd
import pymorphy2
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')

morph = pymorphy2.MorphAnalyzer()
russian_stopwords = stopwords.words("russian")
p = re.compile('[а-яa-z ]+')


def preprocess_text(text):
    tokens = text.lower()
    tokens = "".join(p.findall(tokens))

    tokens = [morph.parse(token)[0].normal_form for token in tokens.split()]

    tokens = [token for token in tokens if token not in russian_stopwords \
              and token != " " \
              and token.strip() not in punctuation]

    text = " ".join(tokens)

    return text


def recommend(df, title, th=0.0):
    title = preprocess_text(title)

    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 1), stop_words=russian_stopwords)
    tfidf_matrix = tf.fit_transform(df['cleaned_desc'].values)

    title_tf = tf.transform([title])

    sig = cosine_similarity(title_tf, tfidf_matrix)

    sig = list(enumerate(sig[0]))

    sig = sorted(sig, key=lambda x: x[1], reverse=True)

    sig = sig[1:6]

    movie_indices = [i[0] for i in sig if i[1] > th]
    rec = df[['obj_name']].iloc[movie_indices]

    return rec


def get_tokens(data, desc_name):
    data['cleaned_desc'] = data[desc_name].copy()
    data['cleaned_desc'] = data.cleaned_desc.apply(func=preprocess_text)
    try:
        data.reset_index(level=0, inplace=True)
    except ValueError:
        print("Cannot insert level_0, already exist")

    return data


def get_rec(path_to_data, name, desc, titles, need_tokens=False):
    data = pd.read_csv(path_to_data)
    if desc != name:
        data_short = data[[name, desc]] if need_tokens else data[[name, desc, 'cleaned_desc']]
        data_short.columns = ['obj_name', 'description'] if need_tokens else ['obj_name', 'description', 'cleaned_desc']
        data_short = data_short.dropna(subset=['description', 'obj_name'])
    else:
        data_short = data.dropna(subset=[name]).drop_duplicates(subset=name)
        data_short = data_short[name] if need_tokens else data_short[[name, 'cleaned_desc']]
        data_short.columns = ['obj_name'] if need_tokens else ['obj_name', 'cleaned_desc']
        data_short = data_short.dropna(subset=['cleaned_desc'])
    if need_tokens:
        data_short = get_tokens(data_short, desc)
    data_short = data_short.dropna(subset=['cleaned_desc'])

    recommendations = []
    for title in titles:
        recs = recommend(data_short, title)
        recommendations.extend(list(recs.index))

    return recommendations

# get_rec('/content/drive/My Drive/Dataset_LCT/books_fin.csv', 'title', 'title', ['Photoshop CS'])

# get_rec('/content/drive/My Drive/Dataset_LCT/events_fin.csv', 'event_name', 'description', ['Photoshop CS'])

# get_rec('/content/drive/My Drive/Dataset_LCT/clubs_fin.csv', 'event_name', 'description', ['Шахматы обучение'])
