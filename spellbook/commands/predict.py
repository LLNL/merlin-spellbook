from types import SimpleNamespace

import click


@click.command()
@click.option(
    "-infile",
    required=False,
    default="new_x.npy",
    type=click.File("rb"),
    help=".npy file with data to predict",
)
@click.option(
    "-reg",
    required=False,
    default="random_forest_reg.pkl",
    type=str,
    help="pickled regressor file",
)
@click.option(
    "-outfile",
    required=False,
    default="new_y.npy",
    type=str,
    help="file to store the new predictions",
)
def cli(infile, reg, outfile):
    """
    Use a regressor to make a prediction
    """
    from spellbook.ml import predict

    args = SimpleNamespace(**{"infile": infile, "reg": reg, "outfile": outfile})
    predict.predict(args)
