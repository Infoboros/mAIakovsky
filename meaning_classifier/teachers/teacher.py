from abc import ABC
from os import path

from keras import Sequential

from language_models import BaseModel
from meaning_classifier.teachers.corpuses import PositiveCorpus, NegativeCorpus
from settings import RAW_MEANING_CLASSIFIER_ROOT, MEANING_CLASSIFIER_ROOT


class Teacher(ABC):
    def __init__(self, meaning_classifier_name: str, dataset_path: [str], embedding: BaseModel):
        self.dataset_path = dataset_path
        self.meaning_classifier_name = meaning_classifier_name
        self.model = self._get_model()
        self.embedding = embedding

    def _get_model(self) -> Sequential:
        raise NotImplemented()

    def get_positive_corpus(self) -> PositiveCorpus:
        return PositiveCorpus()

    def get_negative_corpus(self) -> NegativeCorpus:
        return NegativeCorpus()

    def fit(self):
        self.model.fit()

    def save(self):
        raw_meaning_classifier_path = path.join(RAW_MEANING_CLASSIFIER_ROOT, self.meaning_classifier_name)
        meaning_classifier_path = path.join(MEANING_CLASSIFIER_ROOT, f'{self.meaning_classifier_name}.py')

        self.model.save(raw_meaning_classifier_path)

        # TODO сохранение питон кода
        with open(language_model_path, 'w') as language_model_file:
            language_model_file.write(
                self.get_generate_model()
            )
