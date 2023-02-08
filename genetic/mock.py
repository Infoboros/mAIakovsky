from genetic.population import Population


class MockPopulation(Population):

    def _get_population(self, individuals: []):
        return MockPopulation(individuals, self.embedding, self.fit_function)

    def cross_individual(self, individual):
        if len(individual) == 1:
            return [individual]
        return [individual, individual[:len(individual) - 1]]

    def mutate_individual(self, individual):
        return individual