from corus import load_taiga_proza_metas, load_taiga_proza
from razdel import sentenize, tokenize


class TaigaStihiCorpus:
    def __init__(self, filters: dict):
        # wget https://linghub.ru/static/Taiga/retagged_taiga.tar.gz
        # tar -xzvf retagged_taiga.tar.gz
        path = '/Volumes/UNTITLED/retagged_taiga/stihi_ru.zip'
        metas = load_taiga_proza_metas(path, offset=0, count=1)

        self.filters = filters
        self.records = load_taiga_proza(path, metas, offset=0, count=1)

    def check_filter(self, record) -> bool:
        meta = record.meta
        for field, current_filter in self.filters.items():
            if current_filter in getattr(meta, field):
                return True
        return False

    def __iter__(self):
        print(1)
        while True:
            print(2)
            record = next(self.records)
            print('record')
            if self.filters and not self.check_filter(record):
                print('continue')
                continue
            text = record.text
            for sentence in sentenize(text):
                yield [token.text.lower() for token in tokenize(sentence.text)]
