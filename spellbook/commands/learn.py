##############################################################################
# Copyright (c) Lawrence Livermore National Security, LLC and other
# Merlin-Spellbook Project developers. See top-level LICENSE and COPYRIGHT
# files for dates and other details. No copyright assignment is required to
# contribute to Merlin-Spellbook.
##############################################################################

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
@click.option(
    "-regressor",
    required=False,
    default="RandomForestRegressor",
    type=str,
    help="type of regressor",
)
def cli(infile, x, y, outfile, regressor):
    """
    Use sklearn to make a regressor
    """
    from spellbook.ml import learn_alt as learn

    args = SimpleNamespace(**{"infile": infile, "X": x, "y": y, "outfile": outfile, "regressor": regressor})
    learn.random_forest(args)
