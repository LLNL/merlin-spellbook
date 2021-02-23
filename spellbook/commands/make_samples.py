from types import SimpleNamespace

import click


@click.command()
@click.option(
    "-seed",
    required=False,
    default=None,
    type=int,
    help="random number seed for generating samples",
)
@click.option(
    "-n",
    required=False,
    default=100,
    type=int,
    help="number of samples",
)
@click.option(
    "-dims",
    required=False,
    default=2,
    type=int,
    help="number of dimensions",
)
@click.option(
    "-sample_type",
    required=False,
    default="random",
    type=str,
    help="type of sampling. options: random, grid, lhs, lhd, star, ccf, ccc, cci. If grid, will try to get close to the correct number of samples. for lhd min-max correspond to +- 3 sigma range",
)
@click.option(
    "-scale",
    required=False,
    default=None,
    type=str,
    help='ranges to scale results in form "[(min,max,type),(min, max,type)]" where type = "linear" or "log" (optional: defaults to linear if omitted)',
)
@click.option(
    "-scale_factor",
    required=False,
    default=1.0,
    type=float,
    help="scale factor to appy to all ranges (stacks with -scale)",
)
@click.option(
    "-outfile",
    required=False,
    default="samples",
    type=str,
    help='name of output .npy file',
)
@click.option(
    "-x0",
    required=False,
    default=None,
    type=str,
    help='file with optional point to center samples around, will be added as first entry',
)
@click.option(
    "-x1",
    required=False,
    default=None,
    type=str,
    help='file with x1 to add points between x0 and x1 (non inclusive) along a line',
)
@click.option(
    "-n_line",
    required=False,
    default=100,
    type=int,
    help='number of samples along a line between x0 and x1',
)
@click.option(
    "--hard-bounds",
    required=False,
    default=False,
    type=bool,
    help='force all points to lie within -scale',
)
def cli(seed, n, dims, sample_type, scale, scale_factor, outfile, x0, x1, n_line, hard_bounds):
    """
    Generate some samples!
    """
    from spellbook.sampling import make_samples
    args = SimpleNamespace(
        **{"seed": seed, "n": n, "dims": dims, "sample_type": sample_type, "scale": scale, "scale_factor": scale_factor, "outfile": outfile, "x0": x0, "x1": x1, "n_line": n_line, "hard_bounds": hard_bounds}
    )
    make_samples.process_args(args)

