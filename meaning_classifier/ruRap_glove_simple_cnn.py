
# #
# Данный классификатор смысловой нагруженности сгенерирован автоматически $2023-09-06 16:57:57.319006
# Простая сверточная сеть
# #
from os import path

from settings import RAW_MEANING_CLASSIFIER_ROOT
from meaning_classifier.meaning_classifier import MeaningClassifier
from language_models.ruRap_glove import RurapModelGlove

class RuRapGloveClassifierSimpleCNN(MeaningClassifier):
    def __init__(self):
        super().__init__(path.join(RAW_MEANING_CLASSIFIER_ROOT, 'ruRap_glove_simple_cnn'), RurapModelGlove(), 5)
                    