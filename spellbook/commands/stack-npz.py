from types import SimpleNamespace

import click


@click.command()
@click.option(
    "-f",
    "--force",
    required=False,
    default=False,
    type=bool,
    help="Force write the target file",
)
@click.argument(
    "target",
    required=True,
    type=click.File("wb"),
    #help="target file",
)
@click.argument(
    "source",
    required=True,
    type=str,#TODO nargs="+"
    #help="source files",
)
def cli(infiles, outfile, chunk_size):
    """
    Convert a list of conduit-readable files into a single big conduit node. Simple append, so nodes that already exist will get a name change to conflict-uuid
    """
    from spellbook.data_formatting.conduit.python import collector
    args = SimpleNamespace(
            **{"infiles": infiles, "outfile": outfile, "chunk_size": chunk_size}
    )
    collector.process_args(args)
