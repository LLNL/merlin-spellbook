import argparse
import ast
import sys
from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    RawDescriptionHelpFormatter,
    RawTextHelpFormatter,
)

import numpy as np
import pyDOE as doe
from scipy.stats.distributions import norm

from spellbook.utils import prep_argparse


def scale_samples(samples_norm, limits, limits_norm=(0, 1), do_log=False):
    """Scale samples to new limits, either log10 or linearly.

    Args:
        samples_norm (ndarray): The normalized samples to scale,
            with dimensions (nsamples,ndims).
        limits (list of tuples): A list of (min, max) for the various
            dimensions. Length of list is ndims.
        limits_norm (tuple of floats, optional): The (min, max) from which
            samples_norm were drawn. Defaults to (0,1).
        do_log (boolean or list of booleans, optional): Whether
            to log10 scale each dimension. Either a single boolean or
            a list of length ndims, for each dimension.
            Defaults to ndims*[False].

    Returns:
        ndarray: The scaled samples.

    Note:
        We follow the sklearn convention of requiring samples to be
        given as an (nsamples, ndims) array.

        To transform 1-D arrays:

        >>> samples = samples.reshape((-1,1)) # ndims = 1
        >>> samples = samples.reshape((1,-1)) # nsamples = 1

    Example:

        >>> # Turn 0:1 samples into -1:1
        >>> import numpy as np
        >>> norm_values = np.linspace(0,1,5).reshape((-1,1))
        >>> real_values = scale_samples(norm_values, [(-1,1)])
        >>> print(real_values)
        [[-1. ]
         [-0.5]
         [ 0. ]
         [ 0.5]
         [ 1. ]]
        >>> # Logarithmically scale to 1:10000
        >>> real_values = scale_samples(norm_values, [(1,1e4)] do_log=True)
        >>> print(real_values)
        [[  1.00000000e+00]
         [  1.00000000e+01]
         [  1.00000000e+02]
         [  1.00000000e+03]
         [  1.00000000e+04]]
    """
    norms = np.asarray(samples_norm)
    if len(norms.shape) != 2:
        raise ValueError()
    ndims = norms.shape[1]
    if not hasattr(do_log, "__iter__"):
        do_log = ndims * [do_log]
    logs = np.asarray(do_log)
    lims_norm = np.array([limits_norm for i in logs])
    _lims = []
    for limit, log in zip(limits, logs):
        if log:
            _lims.append(np.log10(limit))
        else:
            _lims.append(limit)
    lims = np.array(_lims)

    slopes = (lims[:, 1] - lims[:, 0]) / (lims_norm[:, 1] - lims_norm[:, 0])
    samples = slopes * (norms - lims_norm[:, 0]) + lims[:, 0]
    samples[:, logs] = pow(10, samples[:, logs])
    return samples


def process_scale(args):
    if args.scale is not None:
        raw = ast.literal_eval(args.scale)
        processed = np.array(raw, dtype=float).tolist()
        return processed


def process_args(args):
    np.random.seed(args.seed)
    n_samples = args.n
    n_dims = args.dims
    hard_bounds = args.hard_bounds
    sample_type = args.sample_type
    if sample_type == "random":
        x = np.random.random((n_samples, n_dims))
    elif sample_type == "grid":
        subdivision = int(pow(n_samples, 1 / float(n_dims)))
        temp = [np.linspace(0, 1.0, subdivision) for i in range(n_dims)]
        X = np.meshgrid(*temp)
        x = np.stack([xx.flatten() for xx in X], axis=1)
    elif sample_type == "lhs":
        x = doe.lhs(n_dims, samples=n_samples)
    elif sample_type == "lhd":
        _x = doe.lhs(n_dims, samples=n_samples)
        x = norm(loc=0.5, scale=0.125).ppf(_x)
    elif sample_type == "star":
        _x = doe.doe_star.star(n_dims)[0]
        x = 0.5 * (_x + 1.0)  # transform to center at 0.5 (range 0-1)
    else:
        raise ValueError(sample_type + " is not a valid choice for sample_type!")

    scales = process_scale(args)

    if scales is not None:
        limits = []
        do_log = []
        for scale in scales:
            limits.append((scale[0], scale[1]))
            if len(scale) < 3:
                scale.append("linear")
            if scale[2] == "log":
                do_log.append(True)
            else:
                do_log.append(False)
        x = scale_samples(x, limits, do_log=do_log)

    # scale the whole box
    x = args.scale_factor * x

    # add x0
    if args.x0 is not None:
        x0 = np.load(args.x0)
        if scales is not None:
            sa = args.scale_factor * np.array(scales)[:, :2].astype("float")
            center = np.mean(sa, axis=1)
        else:
            center = args.scale_factor * 0.5
        # Loop over all x0 points
        all_x = []
        for _x0 in x0:

            _x = x + _x0 - center

            # replace the first entry with x0 for the random ones
            if sample_type == "lhs" or sample_type == "lhd":
                _x[0] = _x0
            else:  # add it for the stencil points
                _x = np.insert(_x, 0, _x0, axis=0)

            if args.x1 is not None:
                x1 = np.load(args.x1)
                line_range = np.linspace(0, 1, args.n_line + 1, endpoint=False)[1:]
                line_samples = _x0 + np.outer(line_range, (x1 - _x0))
                _x = np.vstack((_x, line_samples))
            all_x.append(_x)

        x = np.vstack(all_x)

    if hard_bounds:
        if scales is None:
            x = np.clip(x, 0, 1)
        else:
            for i, dim in enumerate(scales):
                x[:, i] = np.clip(x[:, i], dim[0], dim[1])

    print(x)

    np.save(args.outfile, x)


def setup_argparse(parent_parser=None, the_subparser=None):
    description = "Generate some samples!"
    parser, subparsers = prep_argparse(description, parent_parser, the_subparser)

    # spellbook make-samples
    make_samples = subparsers.add_parser(
        "make-samples",
        help=description,
    )
    make_samples.set_defaults(func=process_args)
    make_samples.add_argument(
        "-seed",
        help="random number seed for generating samples",
        default=None,
        type=int,
    )
    make_samples.add_argument("-n", help="number of samples", default=100, type=int)
    make_samples.add_argument("-dims", help="number of dimensions", default=2, type=int)
    make_samples.add_argument(
        "-sample_type",
        help="type of sampling. options: random, grid, lhs, lhd, star. If grid, will try to get close to the correct number of samples. for lhd min-max correspond to +- 3 sigma range",
        default="random",
    )
    make_samples.add_argument(
        "-scale",
        help='ranges to scale results in form "[(min,max,type),(min, max,type)]" where type = "linear" or "log" (optional: defaults to linear if omitted)',
    )
    make_samples.add_argument(
        "-scale_factor",
        help="scale factor to appy to all ranges (stacks with -scale)",
        type=float,
        default=1.0,
    )
    make_samples.add_argument(
        "-outfile", help="name of output .npy file", default="samples"
    )
    make_samples.add_argument(
        "-x0",
        help="file with optional point to center samples around, will be added as first entry",
        default=None,
    )
    make_samples.add_argument(
        "-x1",
        help="file with x1 to add points between x0 and x1 (non inclusive) along a line",
        default=None,
    )
    make_samples.add_argument(
        "-n_line",
        help="number of samples along a line between x0 and x1",
        default=100,
        type=int,
    )
    make_samples.add_argument(
        "--hard-bounds",
        help="force all points to lie within -scale",
        action="store_true",
    )
    return parser


def main():
    parser = setup_argparse()
    args = parser.parse_args()
    process_args(args)


if __name__ == "__main__":
    sys.exit(main())
