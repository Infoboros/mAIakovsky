from datetime import timedelta, datetime

from corus import load_taiga_stihi, load_taiga_stihi_metas
from razdel import sentenize, tokenize


class TaigaStihiCorpus:
    def __init__(self, filters: dict = None, time_work: timedelta = timedelta(hours=5)):
        # wget https://linghub.ru/static/Taiga/retagged_taiga.tar.gz
        # tar -xzvf retagged_taiga.tar.gz
        self.path = '/Volumes/UNTITLED/retagged_taiga/stihi_ru.zip'

        self.filters = filters
        self.time_work = time_work

    @staticmethod
    def tokenize_sentence_filter(tokenize_sentence: [str]):
        # TODO использовать yargy parser
        return list(
            filter(
                lambda x: (x not in ',:;()./?&!—«»$%@#-+=[]{""}...--***..!') and
                          ('.' not in x) and
                          (',' not in x) and
                          ('/' not in x) and
                          ('.' not in x) and
                          ('!' not in x) and
                          ('*' not in x) and
                          ('-' not in x) and
                          ('\\' not in x),
                tokenize_sentence
            )
        )

    def check_filter(self, record) -> bool:
        meta = record.meta
        for field, current_filter in self.filters.items():
            if current_filter in getattr(meta, field):
                return True
        return False

    def __iter__(self):
        metas = load_taiga_stihi_metas(self.path)
        records = load_taiga_stihi(self.path, metas)

        time_start = datetime.now()
        print(f'Начало обучения: {time_start}')

        while (time_start + self.time_work) > datetime.now():
            try:
                record = next(records)
            except StopIteration:
                print('Дата сет кончился')
                break

            if record.meta and self.filters and not self.check_filter(record):
                continue
            text = record.text
            for sentence in sentenize(text):
                yield self.tokenize_sentence_filter(
                    [token.text.lower() for token in tokenize(sentence.text)]
                )

        print(f'Конец обучения: {datetime.now()}')
