from abc import ABC
from os import path

import numpy as np
from keras.saving.save import load_model

from settings import BASE_PATH
from word2vec_models import Word2VecModel
from word_processing import Word


class MeaningClassifier(ABC):
    def __init__(self, model_file_name: str, embedding: Word2VecModel, window_model_size: int = 5):
        self.model = load_model(
            path.join(
                BASE_PATH,
                'meaning_classifier',
                'saved_classifiers',
                model_file_name
            )
        )
        self.embedding = embedding
        self.window_model_size = window_model_size

    def rate_window(self, window: [Word]) -> float:
        prepared_data = np.array(
            [
                np.array(
                    self.embedding.word2vec(word)
                )
                for word in window
            ]
        )

        return self.model.predict(
            np.array([prepared_data]),
            verbose=0
        )[0][0]

    def classify(self, text: [Word]):
        windows = [
            text[start:start + self.window_model_size]
            for start in range(0, len(text) - self.window_model_size + 1)
        ]

        rates = [
            self.rate_window(window)
            for window in windows
        ]

        finally_rate = sum(rates) / len(rates)
        return finally_rate
