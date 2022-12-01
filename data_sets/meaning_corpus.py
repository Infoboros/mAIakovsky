from abc import ABC

from data_sets.file_base_data_generator import FileBaseDataGenerator


class MeaningCorpus(FileBaseDataGenerator, ABC):

    def _to_string(self, obj) -> str:
        return '|'.join([str(item) for item in obj[0]]) + '/' + str(obj[1])

    def _from_string(self, row: str):
        left, right = row.split('/')
        return (
            [float(item) for item in left.split('|')],
            float(right)
        )

    def __init__(self, embedding, file_path: str, window_size: int = 5):
        super().__init__(file_path)
        self.window_size = window_size
        self.embedding = embedding
