from abc import ABC, abstractmethod

from word_processing import Word


class BaseModel(ABC):

    @abstractmethod
    def predict_next_word(self, context: [Word], count: int = None) -> [str]:
        raise NotImplemented()

    @abstractmethod
    def word2vec(self, word: Word) -> [float]:
        raise NotImplemented()