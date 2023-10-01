import click
from magenta_rapids import validators

def _single_value_if_only_last_mutates(iterable):
    if len(iterable) == 0:
        return
    bastion = iterable[0]
    if len(iterable) == 1:
        return bastion
    if all(bastion == item for item in iterable[:-1]):
        return iterable[-1]
    else:
        raise ValueError(f"Not all elements matched bastion {bastion}. Iterable: {iterable}" +
                         "This may be a problem with the validator for this option.")

def option_valid_midi_file(exists=True):
    if exists:
        help_text = "Absolute path to MIDI file to retrieve from environment."
        callback = lambda ctx, param, value: _single_value_if_only_last_mutates([
            validators.validate_file_exists_in_environment(ctx, param, value),
            validators.validate_file_does_not_exist_at_source(ctx, param, value),
        ])
    else:
        help_text = "Absolute path to MIDI file to store in environment."
        callback = lambda ctx, param, value: _single_value_if_only_last_mutates([
            validators.validate_file_exists_at_source(ctx, param, value),
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
        callback = lambda ctx, param, value: _single_value_if_only_last_mutates([
            validators.validate_magenta_rapids_environment_exists(ctx, param, value),
            validators.construct_environment_from_path_and_backend(ctx, param, value)
        ])
    else:    
        help_text = "Absolute path to root directory in which to create the new Magenta Rapids environment."
        callback = lambda ctx, param, value: _single_value_if_only_last_mutates([
            validators.validate_empty_directory_exists(ctx, param, value)
        ])

    return click.option(
        "--environment_path", "-e",
        help=help_text,
        required=True,
        callback=callback
    )

