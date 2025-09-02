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
    "--infile",
    "-i",
    required=False,
    default="results.npz",
    type=str,
    help=".npz file with X and y data",
)
@click.option(
    "--outfile",
    "-o",
    required=False,
    default="objective_qoi.npz",
    type=str,
    help="npz file to store the objective in",
)
@click.option(
    "--x_names",
    "-x",
    required=False,
    default=None,
    type=str,
    help="variable(s) in infile for the input, defaults to X; can be a comma-delimited list",
)
@click.option(
    "--function",
    "-y",
    required=False,
    default=None,
    type=str,
    help="variable(s) in infile for the output, defaults to y; can be a comma-delimited list",
)
@click.option(
    "--maximize",
    "-m",
    required=False,
    default=False,
    is_flag=True,
    type=bool,
    help="Create a function for maximizing (instead of minimizing, which is default)",
)
@click.option(
    "--constraints",
    "-c",
    required=False,
    default=None,
    type=str,
    help="constraint options to apply, of the form 'g1>1.0,g1<2,g2>4'. Comma-separated string with > or < separating data name and value",
)
def cli(infile, outfile, x_names, function, maximize, constraints):
    """
    Make a "barrier" cost func for constrained opt.

    Note: the 'maximize' flag indicates this is a function that should be maximized, instead of minimized

    Data are stored in a zipped npz file and saved to another zipped file, which contains two fields "X" and "y".
    "X" contains the design variables and "y" contains the new objective.

    Example:

    spellbook make-barrier-cost --infile my_data.npz -x "x0,x1" -y "y" --constraints "g<0,g>-1,h>3.141" --outfile objective.npz

    spellbook learn -infile objective.npz -outfile trained_model.pkl

    python -c "import numpy as np; data = np.load('objective.npz'); print(data['X'][data["y"].argmin())])"

    """
    from spellbook.optimization import qoi

    args = SimpleNamespace(
        **{
            "infile": infile,
            "outfile": outfile,
            "X": x_names,
            "objective": function,
            "maximize_objective": maximize,
            "constraints": constraints,
        }
    )
    qoi.process_args(args)
