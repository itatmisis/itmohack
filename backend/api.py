from backend.ml.ft_inference import ft_embeddings
from backend.ml.graph_inference import inference


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
