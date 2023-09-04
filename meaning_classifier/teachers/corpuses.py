from abc import ABC


class MeaningCorpus(ABC):

    def __init__(self, embedding, file_path: str, window_size: int = 5):
        super().__init__(file_path)
        self.window_size = window_size
        self.embedding = embedding


class PositiveCorpus:
    pass


class NegativeCorpus:
    pass
