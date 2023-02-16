import multiprocessing
from datetime import datetime
from os import path

from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec

from settings import RAW_EMBEDDING_ROOT, LANGUAGE_MODELS_ROOT
from language_models.teachers.teacher import Teacher


class LogCallback(CallbackAny2Vec):
    def __init__(self):
        self.epoch = 0
        self.loss_to_be_subbed = 0

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        loss_now = loss - self.loss_to_be_subbed
        self.loss_to_be_subbed = loss
        print('Loss after epoch {}: {}'.format(self.epoch, loss_now))
        self.epoch += 1


class Word2VecTeacher(Teacher):

    def __init__(self, dataset_name: str, dataset_path: [str]):
        super().__init__(dataset_name, dataset_path)

        cores = multiprocessing.cpu_count()
        self.model = Word2Vec(
            min_count=5,
            window=5,
            vector_size=300,
            workers=cores - 1
        )

    def fit(self):
        data = self.get_data()

        self.model.build_vocab(
            data
        )
        self.model.train(
            data,
            total_examples=self.model.corpus_count,
            epochs=1000,
            compute_loss=True,
            callbacks=[LogCallback()]
        )

    def save(self):
        raw_embedding_path = path.join(RAW_EMBEDDING_ROOT, self.dataset_name)
        language_model_path = path.join(LANGUAGE_MODELS_ROOT, f'{self.dataset_name}.py')

        self.model.save(raw_embedding_path)

        with open(language_model_path, 'w') as language_model_file:
            language_model_file.write(
                f'''# #
# Данная языковая модель сгенерирована автоматически ${datetime.now()}
# #
from os import path

from settings import RAW_EMBEDDING_ROOT
from language_models.word2vec import Word2VecModel

class {self.dataset_name.capitalize()}Model(Word2VecModel):
    def __init__(self):
        super().__init__(path.join(RAW_EMBEDDING_ROOT, '{self.dataset_name}'))
'''
            )
