import re
import string
from functools import partial


def clean_empty(data: [str]):
    return filter(
        lambda row: len(row) > 3,
        data
    )


def remove_r_n(data: [str]) -> [str]:
    return map(
        lambda row: row.replace('\r', '').replace('\n', ' '),
        data
    )


def remove_punctuation_and_lower(data: [str]) -> [str]:
    return map(
        lambda row: row
        .translate(str.maketrans('', '', string.punctuation + '—…–«»' + string.digits))
        .lower(),
        data
    )


def clean(data: [str], main_clean_func) -> [str]:
    return \
        clean_empty(
            main_clean_func(
                remove_punctuation_and_lower(
                    remove_r_n(
                        data
                    )
                )
            )
        )


def remove_tags(data: [str]) -> [str]:
    reg_exp = r'\[([^]]+)\]:?'
    return map(
        lambda row: re.sub(reg_exp, '', row),
        data
    )


def remove_part_names(data: [str]) -> [str]:
    reg_exp = r'куплет \d *|припев *|вступление *|переход *|финал *|pyrokinesis *'
    return map(
        lambda row: re.sub(reg_exp, '', row),
        data
    )


def main_clean_my_song(data: [str]) -> [str]:
    return \
        remove_part_names(
            remove_tags(
                data
            )
        )


clean_my_song = partial(clean, main_clean_func=main_clean_my_song)
