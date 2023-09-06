from os import path

import click

from cli.settings import RAW_DATA_SETS_ROOT
from language_models.ruRap import RurapModel
from meaning_classifier.teachers.simple_convolutional import SimpleConvolutionalTeacher

EMBEDDING_BINDING = {
    'rurap_glove': RurapModel,
    'rurap_rnnlm': RurapModel,
    'rurap_word2vec': RurapModel,
    'rurap_fasttext': RurapModel
}

TEACHER_BINDING = {
    'simple_convolutional': SimpleConvolutionalTeacher
}


@click.command()
@click.option('-d', '--dataset', required=True)
@click.option('-m', '--model', type=click.Choice(list(EMBEDDING_BINDING.keys()), case_sensitive=False), required=True)
@click.option('-t', '--teacher', type=click.Choice(list(TEACHER_BINDING.keys()), case_sensitive=False), required=True)
@click.option('-w', '--window_size', type=click.INT, default=5)
@click.option('-v', '--vec_size', type=click.INT, default=300)
@click.option('-c', '--max_count', type=click.INT, default=100)
def cli(
        dataset: str,
        model: str,
        teacher: str,
        window_size: int = 5,
        vec_size: int = 300,
        max_count: int = 1000
):
    dataset_path = path.join(RAW_DATA_SETS_ROOT, dataset)
    if not path.exists(dataset_path):
        print('Датасет не найден')
        return
    embedding = EMBEDDING_BINDING[model]()
    teacher = TEACHER_BINDING[teacher](
        dataset,
        dataset_path,
        embedding,
        window_size,
        vec_size,
        max_count
    )

    print('Начало обучения')
    teacher.fit()
    print('Конец обучения')

    teacher.save()
    print('Классификатор смысловой нагруженности создан создана')
