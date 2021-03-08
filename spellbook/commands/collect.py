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
@click.option(
    "-outfile",
    required=False,
    default="results.hdf5",
    type=str,
    help="output file",
)
def cli(instring, outfile):
    """
    Collect many json files into a single json file
    """
    from spellbook.data_formatting import collector

    args = SimpleNamespace(**{"instring": instring, "outfile": outfile})
    collector.process_args(args)
