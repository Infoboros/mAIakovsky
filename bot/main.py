from random import randint

import telebot

from generators import Word2VecGenerator
from genetic.genetic import Genetic
from genetic.simple import SimplePopulation
from language_models import TaigaStihiModel
from meaning_classifier import MeaningClassifierCNNTaiga


class Bot:
    def __init__(self, token: str):
        print('Инициализаци...')
        self.bot = telebot.TeleBot(token)

    def definition_consumers(self):
        print('Объявление обработчиков...')

        print('Инициализация языковой модели')
        embedding = TaigaStihiModel()

        print('Инициализация классификатора')
        classifier = MeaningClassifierCNNTaiga()

        @self.bot.message_handler(content_types=['text'])
        def process_text(message):
            base_context = [word for word in message.text.split(' ')]

            generator = Word2VecGenerator(embedding, base_context)

            five_yamb = '_/_/_/_/_/'
            rows_count = randint(2, 4)
            adam = generator.generate(metre_scheme=five_yamb, rows_count=rows_count)
            eve = generator.generate(metre_scheme=five_yamb, rows_count=rows_count)

            population = SimplePopulation([eve, adam, eve], embedding, classifier.classify_paragraph)
            genetic = Genetic(population)
            for generation in range(10):
                print(f'Поколение {generation + 2}')
                genetic.next_population()

            # FIXME
            result = '\n'.join([
                ' '.join(map(str, row))
                for row in genetic.population.population[0]
            ])
            self.bot.send_message(message.from_user.id, result)


    def start_polling(self):
        print('Запуск...')
        self.bot.polling(none_stop=True, interval=0)
