
# #
# Данная языковая модель сгенерирована автоматически $2023-03-30 21:15:46.217051
# Алгоритм RNNLM
# #
from os import path

from settings import RAW_EMBEDDING_ROOT
from language_models.gensim import GensimModel

class RurapModel(GensimModel):
    def __init__(self):
        super().__init__(path.join(RAW_EMBEDDING_ROOT, 'ruRap'))
                    