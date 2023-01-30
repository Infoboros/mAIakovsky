from os import path

from gensim.models import Word2Vec

from settings import DOWNLOADS_PATH
from word_processing import Word
from .base_model import Word2VecModel


class TaigaStihiModel(Word2VecModel):
    def __init__(self):
        self.model = Word2Vec.load(
            path.join(
                DOWNLOADS_PATH,
                'stihi_taiga'
            )
        )
        self.vocab_size = len(self.model.wv.index_to_key)

    def predict_next_word(self, context: [Word], count: int = None) -> [str]:
        return self.model.predict_output_word(
            [word.word for word in context],
            topn=count if count is not None else 100
        ) or []

    def word2vec(self, word: Word) -> [float]:
        return self.model.wv[word.word]
