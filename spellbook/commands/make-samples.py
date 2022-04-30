import click

from spellbook.sampling import make_samples


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
    "--n_samples",
    required=False,
    default=100,
    type=int,
    help="number of samples",
)
@click.option(
    "-dims",
    "--n_dims",
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
    help="scale ranges in form: -scale \"[(min,max,'type'),(min,max,'type')]\" where type: linear or log (type is optional: defaults to linear if omitted)",
)
@click.option(
    "-scale_factor",
    required=False,
    default=1.0,
    type=float,
    help="scale factor to apply to all ranges (stacks with -scale)",
)
@click.option(
    "-outfile",
    required=False,
    default="samples.npy",
    type=str,
    help="name of output .npy file",
)
@click.option(
    "-x0",
    required=False,
    default=None,
    type=str,
    help="file with optional point to center samples around, will be added as first entry",
)
@click.option(
    "-x1",
    required=False,
    default=None,
    type=str,
    help="file with x1 to add points between x0 and x1 (non inclusive) along a line",
)
@click.option(
    "-n_line",
    required=False,
    default=100,
    type=int,
    help="number of samples along a line between x0 and x1",
)
@click.option(
    "--hard-bounds",
    is_flag=True,
    required=False,
    default=False,
    type=bool,
    help="force all points to lie within -scale",
)
def cli(
    seed: int,
    n_samples: int,
    n_dims: int,
    sample_type: str,
    scale: str,
    scale_factor: float,
    outfile: str,
    x0: str,
    x1: str,
    n_line: int,
    hard_bounds: bool,
) -> None:
    """
    Generate some samples!
    """

    sample_generator = make_samples.MakeSamples()
    sample_generator.generate_samples(
        seed,
        n_samples,
        n_dims,
        sample_type,
        scale,
        scale_factor,
        outfile,
        x0,
        x1,
        n_line,
        hard_bounds,
    )
