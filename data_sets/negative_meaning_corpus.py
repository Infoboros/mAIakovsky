from random import choice

from data_sets.meaning_corpus import MeaningCorpus
from data_sets.utils import word_list_to_vec


class NegativeMeaningCorpus(MeaningCorpus):

    def _generate(self, batch_size: int) -> []:
        vocab = self.embedding.model.wv.index_to_key
        for _ in range(batch_size):
            context = [choice(vocab)]
            while True:
                if len(context) >= self.window_size:
                    yield word_list_to_vec(self.embedding, context), 0.0
                    break

                # TODO перенести этот гет в метод модели
                context.append(choice(self.embedding.model.wv.most_similar(context, topn=20))[0])
