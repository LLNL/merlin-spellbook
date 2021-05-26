from types import SimpleNamespace

import click

from spellbook.utils import OptionEatAll


@click.command()
@click.option(
    "-outfile",
    required=False,
    default="filepath_chunks.pkl",
    type=str,
    help="Name of pickle output file.",
)
@click.option(
    "-n_chunks",
    required=False,
    default=1,
    type=int,
    help="Number of chunks/groups to split filepaths up into.",
)
@click.option(
    "-filepaths",
    required=False,
    default="finished_hdf5.txt",
    type=str,
    help="Filepath of txt file containing newline-delimited absolute filepaths to collect",
)
def cli(outfile, n_chunks, filepaths):
    """
    Convert a list of conduit-readable files into conduit node chunks based on groups in '-filepath_chunks'. Simple append, so nodes that already exist will get a name change to conflict-uuid.
    """
    from spellbook.data_formatting import group_files

    args = SimpleNamespace(
        **{
            "outfile": outfile,
            "n_chunks": n_chunks,
            "filepaths": filepaths,
        }
    )
    group_files.process_args(args)
