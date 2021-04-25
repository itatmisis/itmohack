from gensim.models.fasttext import FastText
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import re

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))


class ft_embeddings():
    def __init__(self, path_to_model):
        self.model = FastText.load(path_to_model)
        self.stemmer = WordNetLemmatizer()

    def preprocess_text(self, document):
        document = re.sub(r'\W', ' ', str(document))

        document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)

        document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)

        document = re.sub(r'\s+', ' ', document, flags=re.I)

        document = re.sub(r'^b\s+', '', document)

        document = document.lower()

        tokens = document.split()
        tokens = [self.stemmer.lemmatize(word) for word in tokens]
        tokens = [word for word in tokens if word not in en_stop]
        tokens = [word for word in tokens if len(word) > 3]

        preprocessed_text = ' '.join(tokens)

        word_punctuation_tokenizer = nltk.WordPunctTokenizer()
        word_tokenized_corpus = word_punctuation_tokenizer.tokenize(preprocessed_text)

        return word_tokenized_corpus

    def get_emb(self, corp):
        emb = []
        corp = self.preprocess_text(corp)
        for word in corp:
            try:
                emb.append(self.model.wv[word])
            except:
                pass
        return np.array(emb).mean(axis=0)
