##############################################################################
# Copyright (c) Lawrence Livermore National Security, LLC and other
# Merlin-Spellbook Project developers. See top-level LICENSE and COPYRIGHT
# files for dates and other details. No copyright assignment is required to
# contribute to Merlin-Spellbook.
##############################################################################

import ast

import numpy as np
import pyDOE3 as doe
from scipy.stats import truncnorm
from scipy.stats.distributions import norm

from spellbook.commands import CliCommand


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
    _lims = [np.log10(limit) if log else limit for limit, log in zip(limits, logs)]
    lims = np.array(_lims)

    slopes = (lims[:, 1] - lims[:, 0]) / (lims_norm[:, 1] - lims_norm[:, 0])
    samples = slopes * (norms - lims_norm[:, 0]) + lims[:, 0]
    samples[:, logs] = pow(10, samples[:, logs])
    return samples


def process_scale(scale):
    if scale is not None:
        raw = ast.literal_eval(scale)
        processed = np.array(raw, dtype=float).tolist()
        return processed


def process_round(round):
    if round is not None:
        return round.strip("[|]").replace(" ", "").split(",")


def process_repeat(repeat):
    return repeat.strip("[|]").replace(" ", "").split(",")


def process_array(array, n_dims):
    arr = array.strip("[|]").replace(" ", "").split(",")
    arr = [float(x) for x in arr]
    if len(arr) == 1:
        arr = n_dims * arr
    elif len(arr) != n_dims:
        raise ValueError(f"The processed array must be of length {n_dims} or 1")
    return np.array(arr)


def process_mean_std(n_dims, mean=None, std=None):

    if mean is None:
        mean = np.zeros(n_dims)
    else:
        mean = process_array(mean, n_dims)

    if std is None:
        std = np.ones(n_dims)
    else:
        std = process_array(std, n_dims)

    return mean, std


class MakeSamples(CliCommand):
    def get_samples(self, sample_type, n_samples, n_dims, seed, **kwargs):
        if sample_type == "random":
            x = np.random.random((n_samples, n_dims))
        elif sample_type == "normal":
            mean = kwargs.get("mean", np.zeros(n_dims))
            std = kwargs.get("std", np.ones(n_dims))
            mean, std = process_mean_std(n_dims, mean, std)
            rng = np.random.default_rng(seed)
            x = rng.normal(loc=mean, scale=std, size=(n_samples, n_dims))
        elif sample_type == "truncnorm":
            mean = kwargs.get("mean", np.zeros(n_dims))
            std = kwargs.get("std", np.ones(n_dims))
            lower_std = kwargs.get("lower_std", -2.0)
            upper_std = kwargs.get("upper_std", 2.0)
            mean, std = process_mean_std(n_dims, mean, std)
            x = np.zeros((n_samples, n_dims))
            for d in range(n_dims):
                rv = truncnorm(lower_std, upper_std, loc=mean[d], scale=std[d])
                x[:, d] = rv.rvs(n_samples, random_state=seed)
        elif sample_type == "grid":
            subdivision = int(pow(n_samples, 1 / float(n_dims)))
            temp = [np.linspace(0, 1.0, subdivision) for i in range(n_dims)]
            X = np.meshgrid(*temp)
            x = np.stack([xx.flatten() for xx in X], axis=1)
        elif sample_type == "lhs":
            x = doe.lhs(n_dims, samples=n_samples, random_state=seed)
        elif sample_type == "lhd":
            _x = doe.lhs(n_dims, samples=n_samples, random_state=seed)
            x = norm(loc=0.5, scale=0.125).ppf(_x)
        elif sample_type == "star":
            _x = doe.doe_star.star(n_dims)[0]
            x = 0.5 * (_x + 1.0)  # transform to center at 0.5 (range 0-1)
        elif sample_type == "ccf" or sample_type == "ccc" or sample_type == "cci":
            _x = np.unique(doe.ccdesign(n_dims, face=sample_type), axis=0)
            x = 0.5 * (_x + 1.0)
        else:
            raise ValueError(sample_type + " is not a valid choice for sample_type!")

        return x

    def apply_scale(self, x, scales):
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
        return x

    def apply_rounding(self, x, round):
        if round is not None:
            x = x.astype("object")
            # round the samples
            round = process_round(round)
            values = ["False", "round", "floor", "ceil"]
            # check that the array sizes are the same
            if len(round) != self.n_dims:
                raise ValueError("length of -round must equal value of -dims.")
            for e, r in enumerate(round):
                if r.lower() not in [v.lower() for v in values]:
                    raise ValueError(f"{r} is not an option. Must use {values}.")
                if r.lower() != "false":
                    func = getattr(np, r)
                    x[:, e] = func(x[:, e].astype("float")).astype("int")
        return x

    def apply_repeat(self, x, repeat):
        if repeat is not None:
            repeat = process_repeat(repeat)
            # Check that the values are integers
            try:
                repeat = [int(r) for r in repeat]
            except ValueError:
                raise ValueError(f"one of the values in {repeat} is not in integer format.")
            num_repeat = repeat[0]
            x = np.repeat(x, num_repeat, axis=0)
            if len(repeat) == 2:
                seed_col = repeat[1]
                # Generate and fix seed value to specified column
                s = np.random.rand(self.n_samples) * 10**6
                s = np.round(s).astype("int").tolist()
                s = s * num_repeat
                s = np.array(s)
                # Insert into array for the specified column
                x[:, seed_col] = s[:]
        return x

    def run(
        self,
        seed,
        n,
        dims,
        sample_type,
        scale,
        scale_factor,
        round,
        repeat,
        outfile,
        x0,
        x1,
        n_line,
        hard_bounds,
        mean,
        std,
        lower_std,
        upper_std,
    ):
        np.random.seed(seed)
        self.n_samples = n
        self.n_dims = dims
        hard_bounds = hard_bounds
        sample_type = sample_type

        x = self.get_samples(
            sample_type,
            self.n_samples,
            self.n_dims,
            seed,
            mean=mean,
            std=std,
            lower_std=lower_std,
            upper_std=upper_std,
        )

        scales = process_scale(scale)

        x = self.apply_scale(x, scales)

        # scale the whole box
        x = scale_factor * x

        x = self.apply_rounding(x, round)
        x = self.apply_repeat(x, repeat)

        # add x0
        if x0 is not None:
            x0 = np.atleast_2d(np.load(x0))
            if scales is not None:
                sa = scale_factor * np.array(scales)[:, :2].astype("float")
                center = np.mean(sa, axis=1)
            else:
                center = scale_factor * 0.5
            # Loop over all x0 points
            all_x = []
            for _x0 in x0:

                _x = x + _x0 - center

                # replace the first entry with x0 for the random ones
                if sample_type == "lhs" or sample_type == "lhd":
                    _x[0] = _x0
                else:  # add it for the stencil points
                    _x = np.insert(_x, 0, _x0, axis=0)

                if x1 is not None:
                    x1 = np.load(x1)
                    line_range = np.linspace(0, 1, n_line + 1, endpoint=False)[1:]
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

        np.save(outfile, x)
