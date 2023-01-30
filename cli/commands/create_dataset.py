from sys import stdout
from typing import Optional

import click

from parsers.my_songs import MySongsParser

parser_bindings = {
    'mysongs': MySongsParser
}


@click.command()
@click.option('-u', '--url')
@click.option('-s', '--site', type=click.Choice(list(parser_bindings.keys()), case_sensitive=False), required=True)
@click.option('-o', '--output')
def cli(site: str, url: str, output: Optional[str]):
    parser = parser_bindings[site]()
    parser.parse(url)

    out_stream = open(output) if output is not None else stdout
    parser.save_data(out_stream)
    out_stream.close()
