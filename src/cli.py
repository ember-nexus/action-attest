import click
from .command.run import run


@click.group()
def cli():
    pass


cli.add_command(run)
