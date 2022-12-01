from .meaning_classifier import MeaningClassifier
from word2vec_models import TaigaStihiModel


class MeaningClassifierCNNTaiga(MeaningClassifier):
    def __init__(self):
        super().__init__('CNN_taiga_stihi.h5', TaigaStihiModel())
