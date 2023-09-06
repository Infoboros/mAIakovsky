from abc import ABC, abstractmethod
from functools import reduce
from os import path
from random import shuffle

import numpy as np
import pandas as pd
from keras import Sequential

from language_models import BaseModel
from meaning_classifier.teachers.corpuses import PositiveCorpus, NegativeCorpus, MeaningCorpus
from settings import RAW_MEANING_CLASSIFIER_ROOT, MEANING_CLASSIFIER_ROOT


class Teacher(ABC):
    model_postfix: str
    file_model_postfix: str

    def __init__(self,
                 meaning_classifier_name: str,
                 dataset_path: [str],
                 embedding: BaseModel,
                 window_size: int = 5,
                 vec_size: int = 300,
                 max_count: int = 1000
                 ):
        self.embedding = embedding
        self.window_size = window_size
        self.vec_size = vec_size
        self.max_count = max_count

        self.dataset_path = dataset_path
        self.meaning_classifier_name = meaning_classifier_name
        self.model = self._get_model()

    @abstractmethod
    def _get_model(self) -> Sequential:
        raise NotImplemented()

    @abstractmethod
    def _get_generate_model(self):
        raise NotImplemented()

    def get_positive_corpus(self) -> PositiveCorpus:
        return PositiveCorpus(self.dataset_path, self.embedding, self.window_size, self.max_count)

    def get_negative_corpus(self) -> NegativeCorpus:
        return NegativeCorpus(self.embedding, self.window_size, self.max_count)

    def get_data_from_corpus(self, corpus: MeaningCorpus, result: float) -> [[float], float]:
        iterator = iter(corpus)
        return [
            (np.array(row), np.array(result))
            for row in iterator
        ]

    def prepare_data(self, data):
        shuffle(data)
        validate_barrier = len(data) // 10

        validate, train = data[:validate_barrier], data[validate_barrier:]
        validate_x, validate_y = list(zip(*validate))
        train_x, train_y = list(zip(*train))

        return [
            np.array(values)
            for values in (train_x, train_y, validate_x, validate_y)
        ]

    def _corrref_matr(self, xs, ys):
        flatten_xs = [
            reduce(
                lambda f, s: list(f) + list(s),
                row,
                []
            )
            for row in xs
        ]
        print()

    def data_analytic(self, train_x, train_y, validate_x, validate_y):
        self._corrref_matr(list(train_x) + list(validate_x), list(train_y) + list(validate_y))

    def fit(self):
        positive_corpus = self.get_positive_corpus()
        negative_corpus = self.get_negative_corpus()

        data = self.get_data_from_corpus(positive_corpus, 1.0) + self.get_data_from_corpus(negative_corpus, 0.0)
        train_x, train_y, validate_x, validate_y = self.prepare_data(data)
        self.data_analytic(train_x, train_y, validate_x, validate_y)

        self.history = self.model.fit(
            train_x, train_y,
            batch_size=10,
            epochs=10,
            verbose=1,
            validation_data=(validate_x, validate_y)
        )

    def save(self):
        raw_meaning_classifier_path = path.join(
            RAW_MEANING_CLASSIFIER_ROOT,
            self.meaning_classifier_name + self.file_model_postfix
        )
        meaning_classifier_path = path.join(
            MEANING_CLASSIFIER_ROOT,
            f'{self.meaning_classifier_name}{self.file_model_postfix}.py'
        )

        self.model.save(raw_meaning_classifier_path)

        with open(meaning_classifier_path, 'w') as language_model_file:
            language_model_file.write(
                self._get_generate_model()
            )
