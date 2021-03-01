from types import SimpleNamespace

import click


@click.command()
@click.option(
    "-infile",
    required=False,
    default="results.npz",
    type=str,
    help=".npz file with X and y data",
)
@click.option(
    "-X",
    required=False,
    default=None,
    type=str,
    help="variable(s) in infile for the input, defaults to X; can be a comma-delimited list",
)
@click.option(
    "-y",
    required=False,
    default=None,
    type=str,
    help="variable(s) in infile for the output, defaults to y; can be a comma-delimited list",
)
@click.option(
    "-outfile",
    required=False,
    default="random_forest_reg.pkl",
    type=str,
    help="file to pickle the regressor to",
)
def cli(infile, x, y, outfile):
    """
    Use sklearn to make a regressor
    """
    from spellbook.ml import learn_alt as learn

    args = SimpleNamespace(
        **{
            "infile": infile,
            "X": x,
            "y": y,
            "outfile": outfile,
        }
    )
    learn.random_forest(args)
