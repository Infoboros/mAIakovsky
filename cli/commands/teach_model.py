from os import path

import click

from cli.settings import RAW_DATA_SETS_ROOT

from language_models.teachers import Word2VecTeacher

TEACHER_BINDING = {
    'word2vec': Word2VecTeacher
}

@click.command()
@click.option('-d', '--dataset', required=True)
@click.option('-t', '--teacher', type=click.Choice(list(TEACHER_BINDING.keys()), case_sensitive=False), required=True)
def cli(dataset: str, teacher: str):
    dataset_path = path.join(RAW_DATA_SETS_ROOT, dataset)
    if not path.exists(dataset_path):
        print('Датасет не найден')
        return

    teacher = TEACHER_BINDING[teacher](dataset, dataset_path)

    print('Начало обучения')
    teacher.fit()
    print('Конец обучения')

    teacher.save()
    print('Языковая модель создана')
