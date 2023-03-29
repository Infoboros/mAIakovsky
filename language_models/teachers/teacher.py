from abc import ABC, abstractmethod
from os import path

from razdel import tokenize

from settings import RAW_EMBEDDING_ROOT, LANGUAGE_MODELS_ROOT
from utils import ReusableIter


class Teacher(ABC):
    def __init__(self, dataset_name: str, dataset_path: [str]):
        self.dataset_path = dataset_path
        self.dataset_name = dataset_name

    def _get_data(self) -> [str]:
        with open(self.dataset_path) as dataset:
            while row := dataset.readline():
                yield [
                    word.text
                    for word in tokenize(row)
                ]

    def get_data(self) -> [str]:
        return ReusableIter(self._get_data)

    @abstractmethod
    def fit(self):
        raise NotImplemented()

    @abstractmethod
    def get_generate_model(self):
        raise NotImplemented()

    def save(self):
        raw_embedding_path = path.join(RAW_EMBEDDING_ROOT, self.dataset_name)
        language_model_path = path.join(LANGUAGE_MODELS_ROOT, f'{self.dataset_name}.py')

        self.model.wv.save(raw_embedding_path)

        with open(language_model_path, 'w') as language_model_file:
            language_model_file.write(
                self.get_generate_model()
            )
