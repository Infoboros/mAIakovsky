from abc import ABC, abstractmethod


class FileBaseDataGenerator(ABC):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def generate(self, batch_size: int):
        data = self._generate(batch_size)
        with open(self.file_path, 'a') as f:
            for row in data:
                f.write(
                    self._to_string(row) + '\n'
                )

    def __iter__(self):
        with open(self.file_path, 'r') as f:
            while row := f.readline():
                yield self._from_string(row)

    @abstractmethod
    def _generate(self, batch_size) -> []:
        raise NotImplemented()

    @abstractmethod
    def _to_string(self, obj) -> str:
        raise NotImplemented()

    @abstractmethod
    def _from_string(self, row):
        raise NotImplemented()


