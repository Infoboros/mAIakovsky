import telebot


class Bot:
    def __init__(self, token: str):
        print('Инициализаци...')
        self.bot = telebot.TeleBot(token)

    def definition_consumers(self):
        print('Объявление обработчиков...')

        @self.bot.message_handler(content_types=['text'])
        def process_text(message):
            self.bot.send_message(message.from_user.id, "Хуй")

    def start_polling(self):
        print('Запуск...')
        self.bot.polling(none_stop=True, interval=0)
