from functools import reduce

from language_models import Word2VecModel
from word_processing import Word


def word_list_to_vec(embedding: Word2VecModel, word_list: [str]) -> [float]:
    return list(
        reduce(
            lambda result, word: result + list(embedding.word2vec(Word(word))),
            word_list,
            []
        )
    )