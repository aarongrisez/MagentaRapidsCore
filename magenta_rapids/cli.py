"""
Command-Line Interface
"""

import asyncio
import click
import mido
from magenta_rapids import decorators, backends

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Main entrypoint for CLI
    """


@cli.command()
@decorators.option_valid_environment(exists=False)
def init(environment_path):
    """
    Initialize a Magenta Rapids environment
    """
    click.echo("Initializing a new Magenta Rapids environment in ", nl=False)
    click.secho(environment_path, fg="green", bold=True)
    backend = backends.LocalFileBackend(local_root_path=environment_path)
    backend.initialize()


@cli.command()
@decorators.option_valid_environment()
@decorators.option_valid_midi_file(exists=False)
def store(environment_path, file):
    """
    Store Buffered MIDI in Magenta Rapids format in a given environment
    """
    environment = environment_path
    click.echo("Storing a new file ", nl=False)
    click.secho(file, fg="green", bold=True, nl=False)
    click.echo(" in ", nl=False)
    click.secho(environment, fg="green", bold=True)
    with open(file, "rb") as file_obj:
        full_target_path = environment.store(file_obj)
    click.echo("Successfully stored file ", nl=False)
    click.secho(full_target_path, fg="green", bold=True)


@cli.command()
@decorators.option_valid_environment()
@click.option("-n", "--number_steps", help="Number of times to mutate", default=1, type=int)
def mutate(environment_path, number_steps):
    """
    Mutate MIDI currently stored in Magenta Rapids format in a given environment
    """
    environment = environment_path
    click.echo("Mutating files for Magenta Rapids environment in ", nl=False)
    click.secho(environment, fg="green", bold=True)
    asyncio.run(environment.mutate(number_steps))


@cli.command()
@click.option("-f", "--file", help="MIDI file to play", required=True)
def play(file):
    """
    Mutate MIDI currently stored in Magenta Rapids format in a given environment
    """
    click.echo("Playing ", nl=False)
    click.secho(file, fg="green", bold=True)
    # pylint: disable=no-member
    port = mido.open_output()
    loaded_file = mido.MidiFile(file)
    for msg in loaded_file.play():
        port.send(msg)
