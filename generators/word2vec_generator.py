from random import choices, shuffle

from word_processing.rhymes import Rhymes
from .generator import Generator

from language_models import Word2VecModel
from word_processing import Word


class Word2VecGenerator(Generator):
    def __init__(self, model: Word2VecModel, base_words: [str]):
        super().__init__()
        self.model = model
        self.text = []
        self.base_words = [Word(base_word) for base_word in base_words]

    @staticmethod
    def _mask_metre_scheme(metre_word: str, metre_scheme: str) -> str:

        start_offset = len(metre_scheme) - len(metre_word)

        return ''.join([
            syllable if syllable == '_' else metre_scheme[start_offset + index]
            for index, syllable in enumerate(metre_word)
        ])

    @staticmethod
    def _choice_random_predict(predict_list: [(str, float)]) -> Word:
        words, weights = list(zip(*predict_list))
        return Word(
            choices(words, weights)[0]
        )

    @staticmethod
    def _filter_predict_list(exist_row: [Word], predict_list: [(str, float)]) -> [str]:
        exist_words = [word.word for word in exist_row]
        filtered_word = list(
            filter(
                lambda predict: predict[0] not in exist_words,
                predict_list
            )
        )
        shuffle(filtered_word)
        return filtered_word

    # TODO разбить на маленькие функции
    def _generate_row(self,
                      context: [str],
                      row: [Word],
                      metre_tail: str,
                      with_miss: bool = False
                      ) -> [Word]:
        if not metre_tail:
            return row

        # TODO тут можно поиграться с длинной списка слов
        predict_list = self._filter_predict_list(row, self.model.predict_next_word(context, 100))

        for predict, _ in predict_list:
            word = Word(predict)
            metre = word.metre

            if not metre or (len(metre) > len(metre_tail)):
                continue

            masked_metre = self._mask_metre_scheme(metre, metre_tail)
            if metre_tail.endswith(masked_metre) and \
                    (
                            '/' in metre_tail.removesuffix(masked_metre)
                            or
                            not metre_tail.removesuffix(masked_metre)
                    ):

                if (not row) and \
                        context != self.base_words and \
                        not Rhymes.is_rhyme(word, context[-1]):
                    continue

                generated_row = self._generate_row(
                    context,
                    [word] + row,
                    metre_tail.removesuffix(masked_metre)
                )
                if generated_row is not None:
                    return generated_row

        if with_miss:
            self.statistic.add_miss_metre_record(metre_tail)

            random_predict = self._choice_random_predict(predict_list)
            return self._generate_row(
                context,
                [random_predict] + row,
                # TODO дописать более корректную обработку миса по слогам
                metre_tail[:1]
            )
        else:
            return None

    def _append_row(self, metre_scheme: str) -> None:
        append_row = []
        prev_row = self.text[-1] if self.text else self.base_words

        generated_row = self._generate_row(prev_row, append_row, metre_scheme)
        self.text.append(
            generated_row
            if generated_row is not None
            else self._generate_row(prev_row, append_row, metre_scheme, with_miss=True)
        )

    # TODO добавить передачу схемы рифмования
    def generate(self,
                 rows_count: int = 4,
                 metre_scheme: str = '/_/_/_/_'
                 ):
        self.text = []

        [self._append_row(metre_scheme) for _ in range(rows_count)]

        return self.text
