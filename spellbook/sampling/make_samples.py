import ast
from typing import List, Tuple, Union

import numpy as np
import pyDOE2 as doe
from numpy.typing import NDArray
from scipy.stats.distributions import norm


def scale_samples(
    samples_norm: NDArray,
    limits: List[tuple],
    limits_norm: Tuple[float, float] = (0.0, 1.0),
    do_log: Union[List, bool] = False,
) -> NDArray:
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
        raise ValueError("samples_norm needs to be 2 dimensional")

    ndims = norms.shape[1]
    if not hasattr(do_log, "__iter__"):
        do_log = ndims * [do_log]
    logs = np.asarray(do_log)
    lims_norm = np.array([limits_norm for _ in logs])
    _lims = [np.log10(limit) if log else limit for limit, log in zip(limits, logs)]
    lims = np.array(_lims)

    slopes = (lims[:, 1] - lims[:, 0]) / (lims_norm[:, 1] - lims_norm[:, 0])
    samples = slopes * (norms - lims_norm[:, 0]) + lims[:, 0]
    samples[:, logs] = pow(10, samples[:, logs])
    return samples


def process_scale(scales_str: str) -> Tuple[list, list]:
    """Parse the limits and type of scaling from string input

    Args:
        scales_str (str): argparser input

    Returns:
        Tuple[list, list]: a tuple of the limits and scaling type
    """
    try:
        scales_list = ast.literal_eval(scales_str)
    except ValueError:
        raise ValueError("scale flag not used correctly")

    processed_scales = []
    do_log = []
    for scale in scales_list:
        if len(scale) == 3:
            do_log.append(scale[2] == "log")
        elif len(scale) == 2:
            do_log.append(False)
        else:
            raise ValueError("scale flag not used correctly")
        processed_scales.append((scale[0], scale[1]))

    return (processed_scales, do_log)


class MakeSamples:
    def get_init_samples(self, sample_type: str, n_samples: int, n_dims: int, seed: int) -> NDArray:
        """Generate the initial set of samples

        Args:
            sample_type (str): Type of sampling
            n_samples (int): Number of samples
            n_dims (int): Number of dimensions
            seed (int): Random seed

        Returns:
            NDArray: initial samples
        """
        if sample_type == "random":
            samples = np.random.random((n_samples, n_dims))
        elif sample_type == "grid":
            subdivision = int(pow(n_samples, 1 / float(n_dims)))
            temp = [np.linspace(0, 1.0, subdivision) for _ in range(n_dims)]
            samples_mesh = np.meshgrid(*temp)
            samples = np.stack([xx.flatten() for xx in samples_mesh], axis=1)
        elif sample_type == "lhs":
            samples = doe.lhs(n_dims, samples=n_samples, random_state=seed)
        elif sample_type == "lhd":
            _samples = doe.lhs(n_dims, samples=n_samples, random_state=seed)
            samples = norm(loc=0.5, scale=0.125).ppf(_samples)
        elif sample_type == "star":
            _samples = doe.doe_star.star(n_dims)[0]
            samples = 0.5 * (_samples + 1.0)  # transform to center at 0.5 (range 0-1)
        elif sample_type in ("ccf", "ccc", "cci"):
            _samples = np.unique(doe.ccdesign(n_dims, face=sample_type), axis=0)
            samples = 0.5 * (_samples + 1.0)
        else:
            raise ValueError(f"{sample_type} is not a valid choice for sample_type!")

        return samples

    def generate_samples(
        self,
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
        """Generate and scale samples. Save the samples in outfile

        Args:
            seed (int): Random seed
            n_samples (int): Number of samples
            n_dims (int): Number of dimensions
            sample_type (str): Type of sampling desired
            scale (str): Scale ranges
            scale_factor (float): scale factor to apply to all ranges
            outfile (str): name of output .npy file
            x0 (str): file with optional point to center samples around
            x1 (str): file with x1 to add points between x0 and x1 (non inclusive) along a line
            n_line (int): number of samples along a line between x0 and x1
            hard_bounds (bool): force all points to lie within -scale
        """
        np.random.seed(seed)

        samples = self.get_init_samples(sample_type, n_samples, n_dims, seed)

        scales = None
        if scale:
            scales, do_log = process_scale(scale)
            samples = scale_samples(samples, scales, do_log=do_log)

        # scale the whole box
        samples *= scale_factor

        # add x0
        if x0 is not None:
            x0 = np.atleast_2d(np.load(x0))
            if scales is not None:
                sa = scale_factor * np.array(scales)[:, :2].astype("float")
                center = np.mean(sa, axis=1)
            else:
                center = scale_factor * 0.5
            # Loop over all x0 points
            all_samples = []
            for _x0 in x0:

                _samples = samples + _x0 - center

                # replace the first entry with x0 for the random ones
                if sample_type in ("lhs", "lhd"):
                    _samples[0] = _x0
                else:  # add it for the stencil points
                    _samples = np.insert(_samples, 0, _x0, axis=0)

                if x1 is not None:
                    x1 = np.load(x1)
                    line_range = np.linspace(0, 1, n_line + 1, endpoint=False)[1:]
                    line_samples = _x0 + np.outer(line_range, (x1 - _x0))
                    _samples = np.vstack((_samples, line_samples))
                all_samples.append(_samples)

            samples = np.vstack(all_samples)

        if hard_bounds:
            if scales is None:
                samples = np.clip(samples, 0, 1)
            else:
                for i, dim in enumerate(scales):
                    samples[:, i] = np.clip(samples[:, i], dim[0], dim[1])

        print(samples)

        np.save(outfile, samples)
