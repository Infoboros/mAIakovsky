from gensim.models import KeyedVectors

from word_processing import Word
from .base_model import BaseModel


class GensimModel(BaseModel):
    def __init__(self, path_model: str):
        self.wv = KeyedVectors.load(path_model)

    def predict_next_word(self, context: [Word], count: int = None) -> [str]:
        return self.wv.most_similar(
            [word.word for word in context],
            topn=count if count is not None else 100
        )

    def word2vec(self, word: Word) -> [float]:
        return self.wv[word.word]
