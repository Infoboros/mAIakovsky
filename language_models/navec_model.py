from os import path

from gensim.models import Word2Vec
from navec import Navec

from settings import DOWNLOADS_PATH
from language_models.base_model import BaseModel
from word_processing import Word


class NavecModel(BaseModel):
    def __init__(self):
        navec = Navec.load(
            path.join(
                DOWNLOADS_PATH,
                'navec_hudlit_v1_12B_500K_300d_100q.tar'
            )
        )

        self.model = Word2Vec(vector_size=300)
        keys = navec.vocab.words
        vecs = [[item + 1 for item in navec.get(key)] for key in keys]
        self.model.wv.add_vectors(keys, vecs)
        self.vocab_size = len(self.model.wv.index_to_key)

    def predict_next_word(self, context: [Word], count: int = None) -> [str]:
        return self.model.wv.most_similar(
            [word.word for word in context],
            topn=count if count is not None else self.vocab_size
        )

    def word2vec(self, word: Word) -> [float]:
        return self.model.wv[word.word]
