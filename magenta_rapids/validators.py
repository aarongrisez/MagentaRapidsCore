import click
import os
from magenta_rapids import environment 

def validate_file_exists_in_environment(ctx, name, value):
    if not os.path.isfile(value):
        raise click.BadParameter(f"File {value} does not exist in environment", ctx=ctx, param=name)
    return value

def validate_file_does_not_exist_at_source(ctx, name, value):
    if os.path.isfile(value):
        raise click.BadParameter(f"File {value} already exists at source", ctx=ctx, param=name)
    return value

def validate_file_exists_at_source(ctx, name, value):
    if not os.path.isfile(value):
        raise click.BadParameter(f"File {value} does not exist at source", ctx=ctx, param=name)
    return value

def validate_empty_directory_exists(ctx, name, value):
    if not os.path.isdir(value):
        raise click.BadParameter(f"Directory {value} does not exist", ctx=ctx, param=name)
    for _, dirnames, fnames, _ in os.fwalk(value):
        if dirnames or fnames:
            raise click.BadParameter(f"Directory {value} is not empty", ctx=ctx, param=name)
    return value

def validate_magenta_rapids_environment_exists(ctx, name, value):
    if not os.path.isdir(value):
        raise click.BadParameter(f"Directory {value} does not exist", ctx=ctx, param=name)
    return value

def construct_environment_from_path_and_backend(ctx, name, value):
    if not os.path.isdir(value):
        raise click.BadParameter(f"Directory {value} does not exist", ctx=ctx, param=name)
    return environment.Environment(
        backend=environment.LocalFileBackend(value),
        mutator=environment.SimpleMutator()
    )
