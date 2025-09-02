##############################################################################
# Copyright (c) Lawrence Livermore National Security, LLC and other
# Merlin-Spellbook Project developers. See top-level LICENSE and COPYRIGHT
# files for dates and other details. No copyright assignment is required to
# contribute to Merlin-Spellbook.
##############################################################################

from types import SimpleNamespace

import click


@click.command()
@click.option(
    "-input",
    required=False,
    default="results.json",
    type=str,
    help=".json file with data in it",
)
@click.option(
    "-output",
    required=False,
    default="results.npz",
    type=str,
    help=".npz file with the arrays",
)
@click.option(
    "-schema",
    required=False,
    default="auto",
    type=str,
    help="schema for a single sample that says what data to translate. Defaults to whole first node. Can be a comma-delimited list of subpaths, eg inputs,outputs/scalars,metadata",
)
def cli(input, output, schema):
    """
    Flatten sample json file into numpy", filtering with an external schema.
    """
    from spellbook.data_formatting import translator

    args = SimpleNamespace(**{"input": input, "output": output, "schema": schema})
    translator.process_args(args)
