# #
# Данная языковая модель сгенерирована автоматически $2023-02-18 23:30:36.187361
# #
from os import path

from settings import RAW_EMBEDDING_ROOT
from language_models.word2vec import Word2VecModel

class Ru_rapModel(Word2VecModel):
    def __init__(self):
        super().__init__(path.join(RAW_EMBEDDING_ROOT, 'ru_rap'))
