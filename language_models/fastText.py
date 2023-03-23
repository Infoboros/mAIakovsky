from gensim.models import FastText

from .gensim import GensimModel


class FastTextModel(GensimModel):
    def __init__(self, path_model: str):
        super().__init__(path_model, FastText)
