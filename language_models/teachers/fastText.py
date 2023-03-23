from datetime import datetime

from gensim.models import FastText

from language_models.teachers.gensim import GensimTeacher


class FastTextTeacher(GensimTeacher):

    def __init__(self, dataset_name: str, dataset_path: [str]):
        super().__init__(dataset_name, dataset_path, FastText)

    def get_generate_model(self):
        return \
            f'''
# #
# Данная языковая модель сгенерирована автоматически ${datetime.now()}
# #
from os import path

from settings import RAW_EMBEDDING_ROOT
from language_models.fastText import FastTextModel

class {self.dataset_name.capitalize()}Model(FastTextModel):
    def __init__(self):
        super().__init__(path.join(RAW_EMBEDDING_ROOT, '{self.dataset_name}'))
                    '''