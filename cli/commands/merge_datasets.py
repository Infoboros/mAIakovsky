from os import path

import click

from cli.settings import RAW_DATA_SETS_ROOT


@click.command()
@click.option('-f', '--first_name')
@click.option('-s', '--second_name')
def cli(first_name: str, second_name: str):
    raw_data_set_path_first = path.join(RAW_DATA_SETS_ROOT, first_name)
    raw_data_set_path_second = path.join(RAW_DATA_SETS_ROOT, second_name)
    with open(raw_data_set_path_first, 'r') as first_dataset:
        with open(raw_data_set_path_second, 'a') as output:
            output.write(
                first_dataset.read()
            )
