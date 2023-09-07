
# #
# Данная языковая модель сгенерирована автоматически $2023-09-06 12:14:23.765290
# Алгоритм Word2Vec
# #
from os import path

from settings import RAW_EMBEDDING_ROOT
from language_models.gensim import GensimModel

class RurapModelWord2Vec(GensimModel):
    def __init__(self):
        super().__init__(path.join(RAW_EMBEDDING_ROOT, 'ruRap_word_2_vec'))

