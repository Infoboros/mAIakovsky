from os import path

BASE_PATH = path.dirname(path.abspath(__file__))

DOWNLOADS_PATH = path.join(
    BASE_PATH,
    'downloads'
)


RAW_DATA_SETS_ROOT = path.join(BASE_PATH, 'data_sets', 'raw_data')
RAW_EMBEDDING_ROOT = path.join(BASE_PATH, 'language_models', 'raw_embedding')
LANGUAGE_MODELS_ROOT = path.join(BASE_PATH, 'language_models')
