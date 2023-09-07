from os import path

import click

from cli.settings import RAW_DATA_SETS_ROOT
from language_models.ruRap_word_2_vec import RurapModelWord2Vec
from language_models.ruRap_rnnlm import RurapModelRNNLM
from language_models.ruRap_glove import RurapModelGlove
from language_models.ruRap_fast_text import RurapModelFastText
from meaning_classifier.teachers.simple_convolutional import SimpleConvolutionalTeacher

EMBEDDING_BINDING = {
    'RuRapGlove': (RurapModelGlove, 'RurapModelGlove', 'ruRap_glove', 'ruRap'),
    'RuRapRNNLM': (RurapModelRNNLM, 'RurapModelRNNLM', 'ruRap_rnnlm', 'ruRap'),
    'RuRapWord2Vec': (RurapModelWord2Vec, 'RurapModelWord2Vec', 'ruRap_word_2_vec', 'ruRap'),
    'RuRapFastText': (RurapModelFastText, 'RurapModelFastText', 'ruRap_fast_text', 'ruRap')
}

TEACHER_BINDING = {
    'simple_convolutional': SimpleConvolutionalTeacher
}


@click.command()
@click.option('-m', '--model', type=click.Choice(list(EMBEDDING_BINDING.keys()), case_sensitive=False), required=True)
@click.option('-t', '--teacher', type=click.Choice(list(TEACHER_BINDING.keys()), case_sensitive=False), required=True)
@click.option('-w', '--window_size', type=click.INT, default=5)
@click.option('-v', '--vec_size', type=click.INT, default=300)
@click.option('-c', '--max_count', type=click.INT, default=100)
def cli(
        model: str,
        teacher: str,
        window_size: int = 5,
        vec_size: int = 300,
        max_count: int = 1000
):
    embedding_model, embedding_model_name, embedding_package_name, dataset = EMBEDDING_BINDING[model]
    embedding = embedding_model()
    dataset_path = path.join(RAW_DATA_SETS_ROOT, dataset)
    if not path.exists(dataset_path):
        print('Датасет не найден')
        return

    teacher = TEACHER_BINDING[teacher](
        model,
        embedding_package_name,
        dataset_path,
        embedding,
        embedding_model_name,
        embedding_package_name,
        window_size,
        vec_size,
        max_count
    )

    print('Начало обучения')
    teacher.fit()
    print('Конец обучения')

    teacher.save()
    print('Классификатор смысловой нагруженности создан создана')
