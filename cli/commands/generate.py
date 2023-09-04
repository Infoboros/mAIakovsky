import click

from generators import Word2VecGenerator
from genetic.genetic import Genetic
from genetic.simple import SimplePopulation
from language_models.ruRap import RurapModel
from meaning_classifier import MeaningClassifierCNNTaiga


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
    embedding = RurapModel()
    # TODO вынести параметром
    classifier = MeaningClassifierCNNTaiga()

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
