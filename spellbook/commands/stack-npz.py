from types import SimpleNamespace

import click

from spellbook.data_formatting import stack_npz


@click.command()
@click.option(
    "-f",
    "--force",
    is_flag=True,
    required=False,
    default=False,
    type=bool,
    help="Force write the target file",
)
@click.argument(
    "target",
    required=True,
    type=str,
)
@click.argument(
    "source",
    required=True,
    type=str,
    nargs=-1,
)
def cli(force, target, source):
    """
    Stacker for npz files.
    """

    args = SimpleNamespace(**{"force": force, "target": target, "source": source})
    stack_npz.process_args(args)
