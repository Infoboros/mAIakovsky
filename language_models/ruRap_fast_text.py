
# #
# Данная языковая модель сгенерирована автоматически $2023-09-06 13:18:25.134420
# Алгоритм FastText 
# #
from os import path

from settings import RAW_EMBEDDING_ROOT
from language_models.gensim import GensimModel

class RurapModelFastText(GensimModel):
    def __init__(self):
        super().__init__(path.join(RAW_EMBEDDING_ROOT, 'ruRap_fast_text'))
                    