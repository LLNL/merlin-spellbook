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
@click.option(
    "-infiles",
    required=True,
    type=list,
    cls=OptionEatAll,
    help="whitespace separated list of files to collect",
)
@click.option(
    "-outfile",
    required=False,
    default="results.hdf5",
    type=str,
    help="aggregated file root. If chunking will insert _n before extension",
)
@click.option(
    "-chunk_size",
    required=False,
    default=None,
    type=int,
    help="number of samples per chunk. Default (None): don't chunk",
)
@click.option(
    "-add_uuid",
    required=False,
    default=False,
    is_flag=True,
    help="auto insert a unique id for each file, creating a tree on the fly",
)
def cli(infiles, outfile, chunk_size, add_uuid):
    """
    Convert a list of conduit-readable files into a single big conduit node. Simple append, so nodes that already exist will get a name change to conflict-uuid
    """
    from spellbook.data_formatting.conduit.python import collector

    args = SimpleNamespace(
        **{
            "infiles": infiles,
            "outfile": outfile,
            "chunk_size": chunk_size,
            "add_uuid": add_uuid,
        }
    )
    collector.process_args(args)
