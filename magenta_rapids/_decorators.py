import click
import os

def _single_value_if_all_same_value(iterable):
    if len(iterable) == 0:
        return
    bastion = iterable[0]
    if all(bastion == item for item in iterable):
        return bastion
    else:
        raise ValueError(f"Not all elements matched bastion {bastion}. Iterable: {iterable}" +
                         "This may be a problem with the validator for this option.")

def _validate_file_exists_in_environment(ctx, name, value):
    if not os.path.isfile(value):
        raise click.BadParameter(f"File {value} does not exist in environment", ctx=ctx, param=name)
    return value

def _validate_file_does_not_exist_at_source(ctx, name, value):
    if os.path.isfile(value):
        raise click.BadParameter(f"File {value} already exists at source", ctx=ctx, param=name)
    return value

def _validate_file_exists_at_source(ctx, name, value):
    if not os.path.isfile(value):
        raise click.BadParameter(f"File {value} does not exist at source", ctx=ctx, param=name)
    return value

def _validate_empty_directory_exists(ctx, name, value):
    if not os.path.isdir(value):
        raise click.BadParameter(f"Directory {value} does not exist", ctx=ctx, param=name)
    for _, dirnames, fnames, _ in os.fwalk(value):
        if dirnames or fnames:
            raise click.BadParameter(f"Directory {value} is not empty", ctx=ctx, param=name)
    return value

def _validate_magenta_rapids_environment_exists(ctx, name, value):
    if not os.path.isdir(value):
        raise click.BadParameter(f"Directory {value} does not exist", ctx=ctx, param=name)
    return value

def option_valid_midi_file(exists=True):
    if exists:
        help_text = "Absolute path to MIDI file to retrieve from environment."
        callback = lambda ctx, param, value: _single_value_if_all_same_value([
            _validate_file_exists_in_environment(ctx, param, value),
            _validate_file_does_not_exist_at_source(ctx, param, value),
        ])
    else:
        help_text = "Absolute path to MIDI file to store in environment."
        callback = lambda ctx, param, value: _single_value_if_all_same_value([
            _validate_file_exists_at_source(ctx, param, value),
        ])

    return click.option(
        "-f", "--file", 
        help=help_text,
        required=True,
        callback=callback
    )

def option_valid_environment(exists=True):
    if exists:
        help_text = "Absolute path to root directory of a valid Magenta Rapids environment."
        callback = lambda ctx, param, value: _single_value_if_all_same_value([
            _validate_magenta_rapids_environment_exists(ctx, param, value)
        ])
    else:    
        help_text = "Absolute path to root directory in which to create the new Magenta Rapids environment."
        callback = lambda ctx, param, value: _single_value_if_all_same_value([
            _validate_empty_directory_exists(ctx, param, value)
        ])

    return click.option(
        "-e", "--environment", 
        help=help_text,
        required=True,
        callback=callback
    )