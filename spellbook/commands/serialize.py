##############################################################################
# Copyright (c) Lawrence Livermore National Security, LLC and other
# Merlin-Spellbook Project developers. See top-level LICENSE and COPYRIGHT
# files for dates and other details. No copyright assignment is required to
# contribute to Merlin-Spellbook.
##############################################################################

from types import SimpleNamespace

import click

from spellbook.utils import OptionEatAll


@click.command()
@click.option("--output", required=False, default="output.json", type=str, help="output file")
@click.option(
    "--vars",
    required=False,
    default="spam=cheese monkey=nugget",
    type=list,
    help="variables to write. specified as space separated name=VALUE",
    cls=OptionEatAll,
)
@click.option(
    "--splitter",
    required=False,
    default="/",
    type=str,
    help="key to indicate a nested value, default: /",
)
@click.option(
    "--delimiter",
    required=False,
    default="=",
    type=str,
    help="key to indicate delimiter value, default: =",
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
def cli(output, vars, splitter, delimiter, verbose, indent):
    """
    write a serialized file from cli arguments.
    """
    from spellbook.data_formatting import serialize

    args = SimpleNamespace(
        **{
            "output": output,
            "vars": vars,
            "splitter": splitter,
            "delimiter": delimiter,
            "verbose": verbose,
            "indent": indent,
        }
    )
    serialize.parse_args(args)
