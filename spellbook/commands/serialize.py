from types import SimpleNamespace

import click


@click.command()
@click.option(
    "--output",
    required=False,
    default="output.json",
    type=click.File("wb"),
    help="output file",
)
@click.option(
    "--vars",
    required=False,
    default="results.hdf5",
    type=str, # TODO nargs="+"
    help="variables to write. specified as space separated name=VALUE",
)
@click.option(
    "--splitter",
    required=False,
    default="/",
    type=str,
    help="key to indicate a nested value, default: /",
)
@click.option(
    "--verbose",
    is_flag=True,
    required=False,
    default=False,
    type=bool,
    help="print output, default False",
)
@click.option(
    "--indent",
    is_flag=True,
    required=False,
    default=False,
    type=bool,
    help="indent with new lines, default False",
)
def cli(output, vars, splitter, verbose, indent):
    """
    write a serialized file from cli arguments.
    """
    from spellbook.data_formatting import serialize
    args = SimpleNamespace(
            **{"output": output, "vars": vars, "splitter": splitter, "verbose": verbose, "indent": indent}
    )
    serialize.process_args(args)
