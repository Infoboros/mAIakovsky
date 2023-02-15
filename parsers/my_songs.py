from bs4 import NavigableString

from parsers.cleaners import clean_my_song
from parsers.parser import Parser


class MySongsParser(Parser):

    def __init__(self):
        super().__init__(clean_my_song)

    def parse_songs_links(self, url: str) -> [str]:
        soup = self.get_soup(url)
        text = soup.find('div', {'id': 'text'})
        # Первая ссылка на биографию
        links = text.findAll('a', href=True)[1:]

        base_url = '/'.join(url.split('/')[:-1])
        return [
            f'{base_url}/{link["href"]}'
            for link in links
        ]

    def parse_song(self, url: str):
        soup = self.get_soup(url)


        text = soup.find('div', {'class': 'lyrics'})
        if text is None:
            text = soup.find('div', {'id': 'text'})
        if text is None:
            text = soup.find('div', {'itemprop': 'text'})

        paragraphs = text.findAll('p')
        self.data += [
            ''.join([
                str(content)
                for content in paragraph.contents
                if type(content) is NavigableString
            ])
            for paragraph in paragraphs
        ]

    def parse(self, start_url: str):
        song_urls = self.parse_songs_links(start_url)

        print('Запуск парсинга')
        print(f'Найдено песен {len(song_urls)}')
        count = len(song_urls)

        for index, song_url in enumerate(song_urls):
            print(f'[{index}/{count}] {song_url}')
            self.parse_song(song_url)

        print('Парсинг окончен')
