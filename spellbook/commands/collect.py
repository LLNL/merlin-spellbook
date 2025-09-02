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
    "-instring",
    required=False,
    default="",
    type=str,
    help="whitespace separated list of files to collect",
)
@click.option("-outfile", required=False, default="results.hdf5", type=str, help="output file")
def cli(instring, outfile):
    """
    Collect many json files into a single json file
    """
    from spellbook.data_formatting import collector

    args = SimpleNamespace(**{"instring": instring, "outfile": outfile})
    collector.process_args(args)
