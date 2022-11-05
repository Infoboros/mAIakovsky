class StatisticRecord:
    pass


class MissMetreRecord(StatisticRecord):
    def __init__(self, metre_tail: str):
        self.metre_tail = metre_tail


class Statistic:
    def __init__(self):
        self.records = []

    def __add_record(self, record: StatisticRecord):
        self.records.append(record)

    def add_miss_metre_record(self, metre_tail: str):
        self.__add_record(
            MissMetreRecord(metre_tail)
        )

    def __filter_records_by_type(self, RecordClass):
        return list(
            filter(
                lambda record: isinstance(record, RecordClass),
                self.records
            )
        )

    @property
    def miss_metre_records(self):
        return self.__filter_records_by_type(MissMetreRecord)