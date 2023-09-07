
# #
# Данная языковая модель сгенерирована автоматически $2023-09-06 13:13:51.833163
# Алгоритм RNNLM
# #
from os import path

from settings import RAW_EMBEDDING_ROOT
from language_models.gensim import GensimModel

class RurapModelRNNLM(GensimModel):
    def __init__(self):
        super().__init__(path.join(RAW_EMBEDDING_ROOT, 'ruRap_rnnlm'))
                    