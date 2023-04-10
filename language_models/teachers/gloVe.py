import multiprocessing
from datetime import datetime

from gensim.models import Word2Vec
from glove import Glove
from matplotlib import pyplot as plt

from language_models.teachers.teacher import Teacher


#
# К сожалению автором не был найден репозиторий с реализацией GloVe на PiPy
# Ввиду этого был использована следующая имплементация https://github.com/iconclub/python-glove
#

class GloVeTeacher(Teacher):
    VECTOR_SIZE = 300

    def __init__(self, dataset_name: str, dataset_path: [str]):
        super().__init__(dataset_name, dataset_path)

        cores = multiprocessing.cpu_count()
        teach_start = datetime.now()
        self.model = Glove(
            sentences=self.get_data(),
            min_count=5,
            window=5,
            vector_size=self.VECTOR_SIZE,
            workers=cores - 1,
            verbose=True,
            epochs=10
        )
        print(f'Время обучения: {(teach_start - datetime.now()).seconds} секунд')
        # TODO дописать вывод графика
        traint_log = self.model.get_train_log()
        plt.plot(
            [log['iter'] for log in traint_log],
            [log['cost'] for log in traint_log],
        )

        plt.ylabel('Ошибка')
        plt.xlabel('Номер эпохи')
        plt.show()

    def fit(self):
        print(f'Размер словаря: {len(self.model.wv.index_to_key)} слов')

        word2vec_model = Word2Vec(vector_size=self.VECTOR_SIZE)
        word2vec_model.init_weights()

        keys = self.model.wv.index_to_key
        vecs = self.model.wv.vectors
        word2vec_model.wv.add_vectors(keys, vecs)

        self.model = word2vec_model
        print(f'Оценка памяти необходимой для обучения: {self.model.estimate_memory()}')

        start = datetime.now()
        self.model.predict_output_word(['я', 'тебя', 'люблю'], topn=1000)
        print(f'Время выполнения запроса: {(datetime.now() - start).microseconds} микросекунд')

    def get_generate_model(self):
        return \
            f'''
# #
# Данная языковая модель сгенерирована автоматически ${datetime.now()}
# Алгоритм GloVe
# #
from os import path

from settings import RAW_EMBEDDING_ROOT
from language_models.gensim import GensimModel

class {self.dataset_name.capitalize()}Model(GensimModel):
    def __init__(self):
        super().__init__(path.join(RAW_EMBEDDING_ROOT, '{self.dataset_name}'))
                    '''
