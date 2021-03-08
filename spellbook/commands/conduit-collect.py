from types import SimpleNamespace

import click


@click.command()
@click.option(
    "-infiles",
    required=False,
    default="",
    type=str,
    help="whitespace separated list of files to collect",
)
@click.option(
    "-outfile",
    required=False,
    default="results.hdf5",
    type=click.File("wb"),
    help="aggregated file root. If chunking will insert _n before extension",
)
@click.option(
    "-chunk_size",
    required=False,
    default=None,
    type=int,
    help="number of files to chunk together. Default (None): don't chunk",
)
def cli(infiles, outfile, chunk_size, conduit):
    """
    Convert a list of conduit-readable files into a single big conduit node. Simple append, so nodes that already exist will get a name change to conflict-uuid
    """
    from spellbook.data_formatting.conduit.python import collector

    args = SimpleNamespace(
        **{"infiles": infiles, "outfile": outfile, "chunk_size": chunk_size}
    )
    collector.process_args(args)
