# #
# Данная языковая модель сгенерирована автоматически $2023-09-04 13:52:44.238888
# Алгоритм GloVe
# #
from os import path

from settings import RAW_EMBEDDING_ROOT
from language_models.gensim import GensimModel

class RurapModel(GensimModel):
    def __init__(self):
        super().__init__(path.join(RAW_EMBEDDING_ROOT, 'ruRap'))
                    