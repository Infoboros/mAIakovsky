from genetic.population import Population


class Genetic:
    def __init__(self, population: Population):
        self.population_size = population.size()
        self.population = population
        self.history = []

    def next_population(self) -> Population:
        self.population.crossing()
        self.population.mutating()
        self.population, fit_history = self.population.selection(self.population_size)

        self.history.append(fit_history)

        return self.population