import re
from functools import partial


def clean_empty(data: [str]):
    return filter(
        lambda row: row,
        data
    )


def clean(data: [str], main_clean_func) -> [str]:
    return main_clean_func(
        clean_empty(
            data
        )
    )


def remove_tags(data: [str]) -> [str]:
    reg_exp = r'\[([^]]+)\]:?'
    return map(
        lambda row: re.sub(reg_exp, '', row),
        data
    )

def remove_r_n(data: [str]) -> [str]:
    return map(
        lambda row: row.replace('\r', '').replace('\n', ' '),
        data
    )

def main_clean_my_song(data: [str]) -> [str]:
    return remove_r_n(
        remove_tags(
            data
        )
    )


clean_my_song = partial(clean, main_clean_func=main_clean_my_song)
