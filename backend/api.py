from backend.ml.ft_inference import ft_embeddings
from backend.ml.graph_inference import inference
import pandas as pd


def initialize_fasttext_model(path_to_model="data/ftw.bin"):
    ft_model = ft_embeddings(path_to_model)
    return ft_model


def get_embedings(text):
    ft_model = initialize_fasttext_model()
    emb = ft_model.get_emb(text)
    return emb


def get_graph_ids(embeddings):
    ids = inference(embeddings)
    return ids


def get_citation_metadata():
    file_path = "../data/clear_citation_metadata.csv"
    df = pd.read_csv(file_path)
    return df


def get_articles(ids):
    citations = get_citation_metadata()
    sampled_articles = citations[citations["paper_id"].isin(ids)]
    return sampled_articles


def get_random_articles(amount=10):
    citations = get_citation_metadata()
    sampled_articles = citations.sample(n=amount)
    return sampled_articles
