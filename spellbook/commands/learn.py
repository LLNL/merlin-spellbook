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
    "-outfile",
    required=False,
    default="regressor.pkl",
    type=str,
    help="file to pickle the regressor to",
)
@click.option(
    "-regressor",
    required=False,
    default="RandomForestRegressor",
    type=str,
    help="sklearn regressor type",
)
@click.option(
    "-reg_args",
    required=False,
    default=None,
    type=str,
    help='dictionary of args to pass to the regressor. json format, eg: \'{"n_estimators":3,"max_depth":5}\'',
)
def cli(infile, X, outfile, regressor, reg_args):
    """
    Use sklearn to make a regressor
    """
    from spellbook.ml import learn
    args = SimpleNamespace(
            **{"infile": infile, "X": X, "outfile": outfile, "regressor": regressor, "reg_args": reg_args}
    )
    learn.make_regressor(args)
