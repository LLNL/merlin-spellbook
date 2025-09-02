##############################################################################
# Copyright (c) Lawrence Livermore National Security, LLC and other
# Merlin-Spellbook Project developers. See top-level LICENSE and COPYRIGHT
# files for dates and other details. No copyright assignment is required to
# contribute to Merlin-Spellbook.
##############################################################################

import click


@click.command()
@click.option(
    "-input",
    required=False,
    default="results_features.hdf5",
    type=click.Path(),
    help=".hdf5 file with data in it",
)
@click.option(
    "-output",
    required=False,
    default="results_features.npz",
    type=click.Path(),
    help=".npz file with the arrays",
)
@click.option(
    "-schema",
    required=False,
    default="auto",
    type=str,
    help="schema for a single sample that says what data to translate. Defaults to whole first node. Can be a comma-delimited list of subpaths, eg inputs,outputs/scalars,metadata",
)
@click.option(
    "-chunks",
    required=False,
    default=False,
    type=bool,
    is_flag=True,
    help="Read in all chunked files in the format '<input>_000.hdf5' with n worker processes. Defaults to CPU count. Use -n to specify number of chunks.",
)
@click.option(
    "-n",
    required=False,
    default=None,
    type=int,
    help="Number of processes to translate chunks in parallel. Defaults to CPU count. Use with '-chunks' flag.",
)
def cli(input, output, schema, chunks, n):
    """
    Flatten sample file into another format (conduit-compatible or numpy)", filtering with an external schema.
    """
    from spellbook.data_formatting.conduit.python import translator

    translator.process_args(input, output, schema, chunks, n)
