from .syllables import get_syllables
from .stress import set_stresses


class Word:
    def __init__(self, word: str):
        self.word = word
        self.syllables = self.__init_stresses()

    def __str__(self):
        return self.word

    def __init_stresses(self):
        syllables = get_syllables(self.word)

        set_stresses(syllables, self.word)

        return syllables

    @property
    def metre(self):
        return ''.join([
            '_' if syllable.stress == -1 else '/'
            for syllable in self.syllables
        ])
