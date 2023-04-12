import multiprocessing
from datetime import datetime

import numpy as np
from gensim.models import Word2Vec
from keras import Sequential
from keras.layers import Dense, LSTM, Embedding, GRU, SimpleRNN
from keras_preprocessing.sequence import pad_sequences
from matplotlib import pyplot as plt

from language_models.teachers.teacher import Teacher


class RNNLMTeacher(Teacher):
    VECTOR_SIZE = 300
    WINDOW_SIZE = 5

    def __init__(self, dataset_name: str, dataset_path: [str]):
        super().__init__(dataset_name, dataset_path)

        word2vec = Word2Vec(min_count=1)
        word2vec.build_vocab(self.get_data())

        self.key_to_index = word2vec.wv.key_to_index
        self.index_to_key = word2vec.wv.index_to_key

        self.model = Sequential()

        self.embedding_layer = Embedding(input_dim=len(self.key_to_index.keys()), output_dim=self.VECTOR_SIZE)
        self.model.add(self.embedding_layer)

        self.model.add(GRU(256, return_sequences=True))
        self.model.add(SimpleRNN(128))
        self.model.add(Dense(1))
        self.model.compile(loss='mean_squared_error', metrics=['accuracy'], optimizer='adam')

    def get_indexed_data(self):
        return [
            list(map(lambda word: self.key_to_index[word], row))
            for row in self.get_data()
        ]

    def fit(self):
        teach_start = datetime.now()

        indexed_data = self.get_indexed_data()
        sequence_list = np.array(
            pad_sequences(indexed_data, maxlen=self.WINDOW_SIZE + 1)
        )

        train_text = sequence_list[:, :-1]
        train_predict = sequence_list[:, 1]

        history = self.model.fit(
            train_text,
            train_predict,
            batch_size=10,
            epochs=300,
            validation_split=0.01,
            workers=multiprocessing.cpu_count() - 1,
            use_multiprocessing=True
        )
        print(f'Время обучения: {(teach_start - datetime.now()).seconds} секунд')
        plt.plot(history.history['loss'])
        plt.ylabel('Ошибка')
        plt.xlabel('Номер эпохи')
        plt.show()

        print(f'Размер словаря (Задается константой): {len(self.key_to_index.keys())} слов')

        word2vec_model = Word2Vec(vector_size=self.VECTOR_SIZE)
        word2vec_model.init_weights()
        embedding = self.embedding_layer.get_weights()[0]

        keys = self.index_to_key
        vecs = list(map(list, embedding))
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
# Алгоритм RNNLM
# #
from os import path

from settings import RAW_EMBEDDING_ROOT
from language_models.gensim import GensimModel

class {self.dataset_name.capitalize()}Model(GensimModel):
    def __init__(self):
        super().__init__(path.join(RAW_EMBEDDING_ROOT, '{self.dataset_name}'))
                    '''
