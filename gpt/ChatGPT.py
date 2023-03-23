from settings import GPT_CHAT_TOKEN
from pyChatGPT import ChatGPT as ChatGPTClient


class ChatGPT:
    def __init__(self):
        self.api = ChatGPTClient(GPT_CHAT_TOKEN)

    def rate_poem(self, poem: str) -> str:
        return self.get_answer(
            f'Оцени качество стихотворения:\n'
            f'{poem}'
        )

    def get_answer(self, text: str) -> str:
        resp = self.api.send_message(text)
        return resp['message']
