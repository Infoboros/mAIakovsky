from parsers.parser import Parser


class MySongsParser(Parser):

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

        # TODO дописать взятие текста то что ниже не работает
        text = soup.find('div', {'class': 'lyrics'})
        if text is None:
            text = soup.find('div', {'id': 'text'})
        if text is None:
            text = soup.find('div', {'itemprop': 'text'})

        paragraphs = text.findAll('p', text=True)
        self.data += [
            paragraph.text
            for paragraph in paragraphs
        ]

    def parse(self, start_url: str):
        song_urls = self.parse_songs_links(start_url)
        for song_url in song_urls:
            self.parse_song(song_url)
