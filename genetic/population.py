from abc import ABC, abstractmethod
from word_processing import Word


class Population(ABC):

    def __init__(self, list_individuals: [], embedding, fit_function):
        self.population = list_individuals
        self.embedding = embedding
        self.fit_function = fit_function

    def mutating(self):
        self.population = [
            self.mutate_individual(individual)
            for individual in self.population
        ]

    def crossing(self):
        cross_results = [
            self.cross_individual(individual)
            for individual in self.population
        ]

        new_population = []
        for cross_result in cross_results:
            new_population += cross_result

        self.population = new_population

    @staticmethod
    def filter_copies(individuals: [[[Word]]]) -> [[[Word]]]:

        def equal_individuals(first, second):
            for index_row, row in enumerate(first):
                for index_word, word in enumerate(row):
                    if word.word != second[index_row][index_word]:
                        return False
            return True

        return list(
            filter(
                lambda individual: not any([equal_individuals(individual, other) for other in individuals]),
                individuals
            )
        )

    def selection(self, topn: int):
        fitted_individuals = [
            {
                'rate': self.fit_function(individual),
                'individual': individual
            }
            for individual in self.filter_copies(self.population)
        ]

        fitted_individuals.sort(key=lambda individual: individual['rate'], reverse=True)

        filtered_individuals = fitted_individuals[:topn]

        return self._get_population([rated_individual['individual'] for rated_individual in filtered_individuals]), \
            [rated_individual['rate'] for rated_individual in filtered_individuals]

    @abstractmethod
    def cross_individual(self, individual):
        raise NotImplemented()

    @abstractmethod
    def mutate_individual(self, individual):
        raise NotImplemented()

    @abstractmethod
    def _get_population(self, individuals: []):
        raise NotImplemented()

    def size(self) -> int:
        return len(self.population)

    def print_3d_population(self):
        print(self.__str__())

    def __str__(self):
        result = ""
        for index, individual in enumerate(self.population):
            result += f'Индивид {index}\n'
            for row in individual:
                result += f"{' '.join([str(word) for word in row])}\n"
            result += '\n'
        return result
