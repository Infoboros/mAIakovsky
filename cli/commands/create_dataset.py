from datetime import datetime
from os import path
from sys import stdout
from typing import Optional

import click

from cli.settings import RAW_DATA_SETS_ROOT

from parsers.my_songs import MySongsParser

PARSER_BINFINGS = {
    'mysongs': MySongsParser
}

@click.command()
@click.option('-u', '--url')
@click.option('-n', '--name')
@click.option('-s', '--site', type=click.Choice(list(PARSER_BINFINGS.keys()), case_sensitive=False), required=True)
def cli(site: str, name: str, url: str):
    parser = PARSER_BINFINGS[site]()
    parser.parse(url)

    raw_data_set_path = path.join(RAW_DATA_SETS_ROOT, name)
    with open(raw_data_set_path, 'w') as output:
        parser.save_data(output)
