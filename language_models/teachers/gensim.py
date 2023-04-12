import multiprocessing
from abc import ABC
from datetime import datetime

from gensim.models.callbacks import CallbackAny2Vec
from matplotlib import pyplot as plt

from language_models.teachers.teacher import Teacher


class GensimLogCallback(CallbackAny2Vec):
    def __init__(self):
        self.epoch = 0

        self.loss_to_be_subbed = 0
        self.loss_log = []

        self.start = datetime.now()
        self.end = datetime.now()

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()

        loss_now = loss - self.loss_to_be_subbed
        self.loss_to_be_subbed = loss

        print('Loss after epoch {}: {}'.format(self.epoch, loss_now))
        self.loss_log.append(loss_now)
        self.epoch += 1
        self.end = datetime.now()

    def print_statistic(self):
        time_delta = self.end - self.start
        print(f'Время обучения: {time_delta.seconds} секунд')

        plt.plot(
            [x for x in range(len(self.loss_log))],
            self.loss_log
        )

        # plt.title('Процесс обучения Word2Vec модели')
        plt.ylabel('Ошибка')
        plt.xlabel('Номер эпохи')
        plt.show()


class GensimTeacher(Teacher, ABC):

    def __init__(self, dataset_name: str, dataset_path: [str], Model):
        super().__init__(dataset_name, dataset_path)

        cores = multiprocessing.cpu_count()
        self.model = Model(
            min_count=5,
            window=5,
            vector_size=300,
            workers=cores - 1
        )

    def fit(self):
        data = self.get_data()
        log = GensimLogCallback()

        self.model.build_vocab(
            data
        )
        self.model.train(
            data,
            total_examples=self.model.corpus_count,
            epochs=300,
            compute_loss=True,
            callbacks=[log]
        )

        print(f'Размер словаря: {len(self.model.wv.index_to_key)} слов')
        print(f'Оценка памяти необходимой для обучения: {self.model.estimate_memory()}')
        log.print_statistic()

        start = datetime.now()
        self.model.predict_output_word(['я', 'тебя', 'люблю'], topn=1000)
        print(f'Время выполнения запроса: {(datetime.now() - start).microseconds} микросекунд')
