from data_sets.meaning_corpus import MeaningCorpus
from data_sets.utils import word_list_to_vec


class PositiveMeaningCorpus(MeaningCorpus):

    def __init__(self, data_set, embedding, file_path: str, window_size: int = 5):
        super().__init__(embedding, file_path, window_size)
        self.iter_data_set = iter(data_set)

    def _generate(self, batch_size: int) -> []:
        data = []
        for _ in range(batch_size):
            while len(data) < self.window_size:
                data += next(self.iter_data_set)

            try:
                yield word_list_to_vec(self.embedding, data[:self.window_size]), 1.0
            except KeyError:
                pass

            data = data[self.window_size:]
