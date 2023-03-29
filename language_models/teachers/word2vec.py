from datetime import datetime

from gensim.models import Word2Vec

from language_models.teachers.gensim import GensimTeacher


class Word2VecTeacher(GensimTeacher):

    def __init__(self, dataset_name: str, dataset_path: [str]):
        super().__init__(dataset_name, dataset_path, Word2Vec)

    def get_generate_model(self):
        return \
            f'''
# #
# Данная языковая модель сгенерирована автоматически ${datetime.now()}
# Алгоритм Word2Vec
# #
from os import path

from settings import RAW_EMBEDDING_ROOT
from language_models.gensim import GensimModel

class {self.dataset_name.capitalize()}Model(GensimModel):
    def __init__(self):
        super().__init__(path.join(RAW_EMBEDDING_ROOT, '{self.dataset_name}'))
                    '''