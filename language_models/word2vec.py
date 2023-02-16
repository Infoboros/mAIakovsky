from gensim.models import Word2Vec

from word_processing import Word
from .base_model import BaseModel


class Word2VecModel(BaseModel):
    def __init__(self, path_model: str):
        self.model = Word2Vec.load(path_model)

    def predict_next_word(self, context: [Word], count: int = None) -> [str]:
        return self.model.predict_output_word(
            [word.word for word in context],
            topn=count if count is not None else 100
        )

    def word2vec(self, word: Word) -> [float]:
        return self.model.wv[word.word]
