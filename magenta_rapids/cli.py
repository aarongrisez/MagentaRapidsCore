"""
Command-Line Interface
"""

import click
from magenta_rapids import decode
from magenta_rapids import _decorators as decorators

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass

@cli.command()
@decorators.option_valid_environment(exists=False)
def init(environment):
    """
    Initialize a Magenta Rapids environment
    """
    click.echo("Initializing a new Magenta Rapids environment in ", nl=False)
    click.secho(environment, fg="green", bold=True)

@cli.command()
@decorators.option_valid_environment()
@decorators.option_valid_midi_file(exists=False)
def store(environment, file):
    """
    Store Buffered MIDI in Magenta Rapids format in a given environment
    """
    click.echo("Storing a new file ", nl=False)
    click.secho(file, fg="green", bold=True, nl=False)
    click.echo(" in ", nl=False)
    click.secho(environment, fg="green", bold=True)
    decoded_file = decode.decode_file(environment, file)

@cli.command()
@decorators.option_valid_environment()
@decorators.option_valid_midi_file()
# Leave open the ability to retrieve files by other criteria than just file path
def retrieve(environment, file):
    """
    Retrieve Buffered MIDI from Magenta Rapids format from a given environment
    """
    click.echo("Storing a new file ", nl=False)
    click.secho(file, fg="green", bold=True, nl=False)
    click.echo(" in ", nl=False)
    click.secho(environment, fg="green", bold=True)

@cli.command()
@decorators.option_valid_environment()
def mutate(environment):
    """
    Mutate MIDI currently stored in Magenta Rapids format in a given environment
    """
    click.echo("Mutating files for Magenta Rapids environment in ", nl=False)
    click.secho(environment, fg="green", bold=True)