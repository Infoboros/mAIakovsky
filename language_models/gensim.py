from word_processing import Word
from .base_model import BaseModel


class GensimModel(BaseModel):
    def __init__(self, path_model: str, Model):
        self.model = Model.load(path_model)

    def predict_next_word(self, context: [Word], count: int = None) -> [str]:
        return self.model.predict_output_word(
            [word.word for word in context],
            topn=count if count is not None else 100
        )

    def word2vec(self, word: Word) -> [float]:
        return self.model.wv[word.word]
