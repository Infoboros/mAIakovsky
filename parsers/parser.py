from abc import ABC, abstractmethod

from io import TextIOWrapper

import requests
from bs4 import BeautifulSoup


class Parser(ABC):

    @staticmethod
    def get_soup(url: str) -> BeautifulSoup:
        response = requests.get(url)
        return BeautifulSoup(response.text, features='lxml')

    def __init__(self, clean_function):
        self.data: [str] = []
        self.clean_function = clean_function

    @abstractmethod
    def parse(self, start_url: str):
        raise NotImplemented()

    def save_data(self, output: TextIOWrapper) -> int:
        return output \
            .write(
                '\n'.join(
                    self.clean_function(
                        self.data
                    )
                )
        )