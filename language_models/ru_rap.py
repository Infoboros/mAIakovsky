
# #
# Данная языковая модель сгенерирована автоматически $2023-03-24 00:05:39.210529
# #
from os import path

from settings import RAW_EMBEDDING_ROOT
from language_models.fastText import FastTextModel

class Ru_rapModel(FastTextModel):
    def __init__(self):
        super().__init__(path.join(RAW_EMBEDDING_ROOT, 'ru_rap'))
                    