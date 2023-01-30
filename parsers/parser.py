from abc import ABC, abstractmethod

from io import TextIOWrapper

import requests
from bs4 import BeautifulSoup


class Parser(ABC):

    @staticmethod
    def get_soup(url: str) -> BeautifulSoup:
        response = requests.get(url)
        return BeautifulSoup(response.text, features='lxml')

    def __init__(self):
        self.data: [str] = []

    @abstractmethod
    def parse(self, start_url: str):
        raise NotImplemented()

    def save_data(self, output: TextIOWrapper) -> int:
        return output \
            .write('\n'.join(self.data))