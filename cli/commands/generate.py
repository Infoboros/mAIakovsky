import click
import matplotlib.pyplot as plt

from generators import Word2VecGenerator
from genetic.genetic import Genetic
from genetic.simple import SimplePopulation
from language_models.ruRap_glove import RurapModelGlove
from meaning_classifier.ruRap_glove_simple_cnn import RuRapGloveClassifierSimpleCNN


# TODO дописать параметры
@click.command()
@click.option('-c', '--context', required=True, type=click.STRING)
@click.option('-m', '--metre_scheme', type=click.STRING, default='/__/_/__')
@click.option('-r', '--rows_count', type=click.INT, default=4)
def cli(
        context: str,
        metre_scheme: str,
        rows_count: int
):
    prepared_context = list(map(
        lambda word: word.lower(),
        context.split(',')
    ))
    # TODO вынести параметром
    embedding = RurapModelGlove()
    # TODO вынести параметром
    classifier = RuRapGloveClassifierSimpleCNN()

    generator = Word2VecGenerator(embedding, prepared_context)
    population = SimplePopulation(
        [
            generator.generate(metre_scheme=metre_scheme, rows_count=rows_count),
            generator.generate(metre_scheme=metre_scheme, rows_count=rows_count)
        ],
        embedding,
        classifier.classify_paragraph
    )
    print(population)

    genetic = Genetic(population)
    for generation in range(10):
        print(f'Поколение {generation + 2}')
        print(genetic.next_population())

    xs = range(len(genetic.history))
    history = list(zip(*genetic.history))
    for individual in history:
        plt.plot(xs[2:], individual[2:])

    plt.title('Процесс селекции')
    plt.ylabel('Критерий смысла')
    plt.xlabel('Номер эпохи')
    plt.legend([index + 1 for index in range(len(history))], loc='upper left')
    plt.show()
