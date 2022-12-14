from .meaning_classifier import MeaningClassifier
from word2vec_models import NavecModel


class MeaningClassifierCNNNavec(MeaningClassifier):
    def __init__(self):
        super().__init__('meaning_classifier_navec_CNN.h5', NavecModel())
