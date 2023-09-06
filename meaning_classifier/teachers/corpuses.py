from abc import ABC, abstractmethod
from random import choice

from language_models import BaseModel
from word_processing import Word


class MeaningCorpus(ABC):

    def __init__(self, embedding: BaseModel, window_size: int = 5, max_count: int = 1000):
        self.window_size = window_size
        self.embedding = embedding
        self.max_count = max_count

    @abstractmethod
    def _get_data(self) -> [Word]:
        raise NotImplemented()

    def _row_to_vec(self, row: [Word]) -> [[float]]:
        return [
            self.embedding.word2vec(word)
            for word in row
        ]

    def batch_words(self, row: [Word]) -> [[Word]]:
        for x in range(0, len(row) - self.window_size + 1):
            e_c = row[x: self.window_size + x]

            if len(e_c) == self.window_size:
                yield e_c

    def __iter__(self):
        counter = 0
        while row := self._get_data():
            for batch in self.batch_words(row):
                try:
                    yield self._row_to_vec(batch)
                except KeyError:
                    pass

                counter += 1
                if counter > self.max_count:
                    return


class PositiveCorpus(MeaningCorpus):
    def _get_data(self) -> [Word]:
        row = self.dataset.readline()
        if row:
            return [Word(word) for word in row.split()]
        self.dataset.close()
        self.dataset = open(self.dataset_path)

    def __del__(self):
        self.dataset.close()

    def __init__(self,
                 dataset_path: str,
                 embedding: BaseModel,
                 window_size: int = 5,
                 max_count: int = 1000, ):
        super().__init__(embedding, window_size, max_count)
        self.dataset_path = dataset_path
        self.dataset = open(self.dataset_path)


class NegativeCorpus(MeaningCorpus):

    def _get_data(self) -> [Word]:
        self.context = [
            Word(word)
            for word, weight in self.embedding.predict_next_word(self.context, self.window_size)
        ]
        return self.context

    def __init__(self,
                 embedding: BaseModel,
                 window_size: int = 5,
                 max_count: int = 1000, ):
        super().__init__(embedding, window_size, max_count)
        self.context = [
            Word(choice(embedding.vocab))
            for _ in range(window_size)
        ]
