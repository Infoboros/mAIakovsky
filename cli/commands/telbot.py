import click

from bot import Bot


@click.command()
@click.option('-t', '--token', required=True)
def cli(token: str):
    bot = Bot(token)
    bot.definition_consumers()
    bot.start_polling()
