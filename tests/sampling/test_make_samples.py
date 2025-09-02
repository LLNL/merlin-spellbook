##############################################################################
# Copyright (c) Lawrence Livermore National Security, LLC and other
# Merlin-Spellbook Project developers. See top-level LICENSE and COPYRIGHT
# files for dates and other details. No copyright assignment is required to
# contribute to Merlin-Spellbook.
##############################################################################

"""
Checks for various ranges of values to sample for both linear and log scaling.
"""

import numpy as np
import numpy.testing

from spellbook.sampling.make_samples import scale_samples


def test_scale_samples_nolog_1():

    # Turn 0:1 samples into -1:1

    norm_values = np.linspace(0, 1, 5).reshape((-1, 1))
    real_values = scale_samples(norm_values, [(-1, 1)])
    expected = np.array([[-1.0], [-0.5], [0.0], [0.5], [1.0]])

    print("real------------------------------")
    print(real_values)
    print("expected------------------------------")
    print(expected)

    numpy.testing.assert_array_equal(real_values, expected)


def test_scale_samples_nolog_2():

    # Turn 0:1 samples into -1:10

    norm_values = np.linspace(0, 1, 10).reshape((-1, 10))
    real_values = scale_samples(norm_values, [(-1, 1)])
    expected = [[-1.0, -0.77, -0.55, -0.33, -0.11, 0.11, 0.33, 0.55, 0.77, 1]]

    print("real------------------------------")
    print(real_values)
    print("expected------------------------------")
    print(expected)

    numpy.testing.assert_allclose(real_values, expected, rtol=0.02, atol=0, verbose=True)


# Turn 0:1 samples into 1:10 with log scaling
def test_scale_samples_log_1():
    norm_values = np.linspace(0, 1, 5).reshape((1, 5))
    real_values = scale_samples(norm_values, [(1, 10)], do_log=True)
    print("real------------------------------")
    print(real_values)
    expected = [[1.0, 1.77, 3.16, 5.62, 10.0]]
    print("expected------------------------------")
    print(expected)
    numpy.testing.assert_allclose(real_values, expected, rtol=0.02, atol=0, verbose=True)
