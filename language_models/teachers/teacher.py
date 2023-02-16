from abc import ABC, abstractmethod

from razdel import tokenize

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
    def save(self):
        raise NotImplemented()
