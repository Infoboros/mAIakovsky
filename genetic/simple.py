from random import randint, choices

from genetic.population import Population
from word_processing import Word


def copy(matrix):
    return [
        [item for item in row]
        for row in matrix
    ]


class SimplePopulation(Population):

    def _get_population(self, individuals: []):
        return SimplePopulation(individuals, self.embedding, self.fit_function)

    def cross_individual(self, individual):
        return [
            copy(individual),
            copy(individual)
        ]

    @staticmethod
    def equal_metres(word_metre: str, predict_metre: str) -> bool:
        if len(word_metre) != len(predict_metre):
            return False

        for index, syllable in enumerate(word_metre):
            predict_syllable = predict_metre[index]
            if (predict_syllable != '/') and (predict_syllable != syllable):
                return False

        return True

    def mutate_individual(self, individual):
        def mutate_word(word: Word):
            if randint(1, 10) == 3:
                word_metre = word.metre
                predicted_words = self.embedding.predict_next_word([word], 20)
                metre_approved_words = list(
                    filter(
                        lambda predicted_word: self.equal_metres(word_metre, Word(predicted_word[0]).metre),
                        predicted_words
                    )
                )
                if metre_approved_words:
                    words, weights = list(zip(*metre_approved_words))
                    return Word(
                        choices(words, weights)[0]
                    )
            return word

        return [
            [
                mutate_word(word)
                for word in row
            ]
            for row in individual
        ]