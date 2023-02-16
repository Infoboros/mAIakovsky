from functools import reduce

from language_models import BaseModel
from word_processing import Word


def word_list_to_vec(embedding: BaseModel, word_list: [str]) -> [float]:
    return list(
        reduce(
            lambda result, word: result + list(embedding.word2vec(Word(word))),
            word_list,
            []
        )
    )