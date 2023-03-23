from gensim.models import Word2Vec

from .gensim import GensimModel


class Word2VecModel(GensimModel):
    def __init__(self, path_model: str):
        super().__init__(path_model, Word2Vec)
