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
    stacker for npz files.
    """
    from spellbook.data_formatting import stack_npz
    args = SimpleNamespace(
            **{"force": force, "target": target, "source": source}
    )
    stack_npz.process_args(args)
