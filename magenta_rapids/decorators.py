"""Collection of decorators for use with the Magenta Rapids CLI.
"""

import click
from magenta_rapids import validators


def _single_value_if_only_last_mutates(iterable):
    """Function which takes an iterable of functions and returns the last value if
    all other values are equal. Otherwise, it raises a ValueError. This is useful
    for click callbacks which are composed of multiple validators, where we want
    just the last validator to mutate the input.
    """
    if len(iterable) == 0:
        raise ValueError("Must provide a nonempty iterable.")
    bastion = iterable[0]
    if len(iterable) == 1:
        return bastion
    if all(bastion == item for item in iterable[:-1]):
        return iterable[-1]
    raise ValueError(
        f"Not all elements matched bastion {bastion}. Iterable: {iterable}"
        + "This may be a problem with the validator for this option."
    )


def option_valid_midi_file(exists=True):
    """Check that the given MIDI file either exists or does not exist, depending on
    the value of the `exists` parameter. If `exists=True`, check that it does not
    already exist in the environment. If `exists=False` check that it does exist
    at the given location.
    """
    if exists:
        help_text = "Absolute path to MIDI file to retrieve from environment."
        def _callback(ctx, param, value):
            return _single_value_if_only_last_mutates(
                [
                    validators.validate_file_exists_in_environment(ctx, param, value),
                    validators.validate_file_does_not_exist_at_source(ctx, param, value),
                ]
            )
    else:
        help_text = "Absolute path to MIDI file to store in environment."
        def _callback(ctx, param, value):
            return _single_value_if_only_last_mutates(
                [
                    validators.validate_file_exists_at_source(ctx, param, value),
                ]
            )

    return click.option(
        "-f", "--file", help=help_text, required=True, callback=_callback
    )


def option_valid_environment(exists=True):
    """Check that the given environment either exists or does not exist, depending on
    the value of the `exists` parameter. If `exists=True`, check that a valid Magenta
    Rapids environment exists at the given location and return it. If `exists=False`
    check that the given location is an empty directory and return a new environment
    at that location.
    """
    if exists:
        help_text = (
            "Absolute path to root directory of a valid Magenta Rapids environment."
        )
        def _callback(ctx, param, value):
            return _single_value_if_only_last_mutates(
                [
                    validators.validate_magenta_rapids_environment_exists(
                        ctx, param, value
                    ),
                    validators.construct_environment_from_path_and_backend(
                        ctx, param, value
                    ),
                ]
            )
    else:
        help_text = (
            "Absolute path to root directory in which to create the new Magenta Rapids Environment"
        )
        def _callback(ctx, param, value):
            return _single_value_if_only_last_mutates(
                [validators.validate_empty_directory_exists(ctx, param, value)]
            )

    return click.option(
        "--environment_path", "-e", help=help_text, required=True, callback=_callback
    )
