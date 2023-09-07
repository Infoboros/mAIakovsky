from datetime import datetime

from keras import Sequential
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Conv2D, MaxPooling2D, Normalization

from meaning_classifier.teachers.teacher import Teacher


class SimpleConvolutionalTeacher(Teacher):
    model_postfix: str = 'SimpleCNN'
    file_model_postfix: str = '_simple_cnn'

    def _get_model(self) -> Sequential:
        model = Sequential()
        model.add(
            Conv2D(
                300,
                (5, 5),
                input_shape=(self.window_size, self.vec_size, 1),
                activation='relu',
                padding='same'
            )
        )
        model.add(MaxPooling2D((1, 3), padding='valid'))
        model.add(
            Conv2D(
                100,
                (5, 5),
                activation='relu',
                padding='same'
            )
        )
        model.add(MaxPooling2D(pool_size=(1, 2), padding='valid'))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy', metrics=['accuracy'], optimizer='adam')
        return model

    def _get_generate_model(self):
        return \
            f'''
# #
# Данный классификатор смысловой нагруженности сгенерирован автоматически ${datetime.now()}
# Простая сверточная сеть
# #
from os import path

from settings import RAW_MEANING_CLASSIFIER_ROOT
from meaning_classifier.meaning_classifier import MeaningClassifier
from language_models.{self.embedding_package_name} import {self.embedding_model_name}

class {self.meaning_classifier_name}Classifier{self.model_postfix}(MeaningClassifier):
    def __init__(self):
        super().__init__(path.join(RAW_MEANING_CLASSIFIER_ROOT, '{self.meaning_classifier_path}{self.file_model_postfix}'), {self.embedding_model_name}(), {self.window_size})
                    '''
