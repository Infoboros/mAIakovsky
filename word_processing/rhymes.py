from word_processing import Word


# TODO ввести систему оценки рифмы и выбирать более красивые
class Rhymes:

    @staticmethod
    def is_rhyme(word1: Word, word2: Word) -> bool:
        return word1.syllables[-1].text == word2.syllables[-1].text
