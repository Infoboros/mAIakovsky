
# #
# Данная языковая модель сгенерирована автоматически $2023-03-29 23:18:58.935326
# #
from os import path

from settings import RAW_EMBEDDING_ROOT
from language_models.gensim import GensimModel

class RurapModel(GensimModel):
    def __init__(self):
        super().__init__(path.join(RAW_EMBEDDING_ROOT, 'ruRap'))
                    