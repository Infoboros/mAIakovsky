from .statistic import Statistic

class Generator:

    def __init__(self):
        self.statistic = Statistic()

    class NotFoundWords(Exception):
        def __init__(self):
            super().__init__('Не найдено подходящих слов')
