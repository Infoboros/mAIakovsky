from random import randint

import telebot

from generators import Word2VecGenerator
from genetic.genetic import Genetic
from genetic.simple import SimplePopulation
from gpt import ChatGPT
from language_models.ru_rap import Ru_rapModel


# from meaning_classifier import MeaningClassifierCNNTaiga


class Bot:
    def __init__(self, token: str):
        print('Инициализация...')
        self.bot = telebot.TeleBot(token)

        print('Инициализация ChatGPT...')
        self.gpt = ChatGPT()

        print('Инициализация языковой модели')
        self.embedding = Ru_rapModel()

        # print('Инициализация классификатора')
        # self.classifier = MeaningClassifierCNNTaiga()

    def __generate_text(self, context: [str]) -> str:
        prepared_context = list(map(
            lambda word: word.lower(),
            context
        ))
        generator = Word2VecGenerator(self.embedding, prepared_context)

        five_yamb = '/__/_/__'
        rows_count = 2
        adam = generator.generate(metre_scheme=five_yamb, rows_count=rows_count)
        eve = generator.generate(metre_scheme=five_yamb, rows_count=rows_count)

        return '\n'.join([
            ' '.join(map(str, row))
            for row in [
                adam[0],
                eve[0],
                adam[1],
                eve[1]
            ]
        ])
        # population = SimplePopulation([eve, adam, eve], embedding, classifier.classify_paragraph)
        # genetic = Genetic(population)
        # for generation in range(10):
        #     print(f'Поколение {generation + 2}')
        #     genetic.next_population()

    def __rate_text(self, text: str) -> str:
        return self.gpt.rate_poem(text)

    def definition_consumers(self):
        print('Объявление обработчиков...')

        @self.bot.message_handler(content_types=['text'])
        def process_text(message):
            command, *text = message.text.split('\n')

            if command.lower() == 'gen':
                output = self.__generate_text(' '.join(text).split(' '))
            else:
                output = self.__rate_text('\n'.join([command, *text]))

            self.bot.send_message(message.from_user.id, output)

    def start_polling(self):
        print('Запуск...')
        self.bot.polling(none_stop=True, interval=0)
