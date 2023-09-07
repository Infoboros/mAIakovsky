
# #
# Данная языковая модель сгенерирована автоматически $2023-09-06 13:15:07.506889
# Алгоритм GloVe
# #
from os import path

from settings import RAW_EMBEDDING_ROOT
from language_models.gensim import GensimModel

class RurapModelGlove(GensimModel):
    def __init__(self):
        super().__init__(path.join(RAW_EMBEDDING_ROOT, 'ruRap_glove'))
                    