# #
# Данная языковая модель сгенерирована автоматически $2023-02-17 22:40:14.022249
# #
from os import path

from settings import RAW_EMBEDDING_ROOT
from language_models.word2vec import Word2VecModel

class Ru_rapModel(Word2VecModel):
    def __init__(self):
        super().__init__(path.join(RAW_EMBEDDING_ROOT, 'ru_rap'))
