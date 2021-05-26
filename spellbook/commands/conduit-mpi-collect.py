from types import SimpleNamespace

import click

from spellbook.utils import OptionEatAll


@click.command()
@click.option(
    "-outfile",
    required=False,
    default="results.hdf5",
    type=str,
    help="aggregated file root. If chunking will insert _n before extension",
)
@click.option(
    "-add_uuid",
    required=False,
    default=False,
    is_flag=True,
    help="auto insert a unique id for each file, creating a tree on the fly",
)
@click.option(
    "-filepath_chunks",
    required=False,
    default="filepath_chunks.pkl",
    type=str,
    help="point to serialized file containing list of lists of filenames (chunks)"
)
def cli(outfile, add_uuid, filepath_chunks):
    """
    Convert a list of conduit-readable files into a single big conduit node. Simple append, so nodes that already exist will get a name change to conflict-uuid
    """
    from spellbook.data_formatting.conduit.python import mpi_collector

    args = SimpleNamespace(
        **{
            "outfile": outfile,
            "add_uuid": add_uuid,
            "filepath_chunks": filepath_chunks,
        }
    )
    mpi_collector.process_args(args)
