from .syllables import Syllable

# TODO сделать что нибудь свое и нормальное
from .russian_accentuation.stress import load, accentuate

lemmas, wordforms = load()

def set_stresses(syllables: [Syllable], word: str):
    # TODO заменить на что нибудь более приличное чем глобавльная переменная
    # TODO возможно стоит анализировать и контекст слова для нормального опредления ударения
    stresses = accentuate(word, wordforms, lemmas)

    if len(syllables) == 1:
        syllables[0].stress = 1
    else:
        for syllable in syllables:
            stesses_syllable = stresses[syllable.begin:syllable.end]
            text_syllable = syllable.text

            syllable.stress = 1 if stesses_syllable != text_syllable else -1

    return syllables

