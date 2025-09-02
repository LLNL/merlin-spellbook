##############################################################################
# Copyright (c) Lawrence Livermore National Security, LLC and other
# Merlin-Spellbook Project developers. See top-level LICENSE and COPYRIGHT
# files for dates and other details. No copyright assignment is required to
# contribute to Merlin-Spellbook.
##############################################################################

import os

import numpy as np

from spellbook.utils import stack_arrays


def test_stack_arrays():
    data1 = np.random.random((3, 2))
    data2 = np.zeros((3, 2))
    data3 = np.ones((3, 2))
    np.savez("temp.npz", F1=data1, F2=data2, F3=data3)
    loaded = np.load("temp.npz")
    os.remove("temp.npz")
    feature_names = "F1,F2,F3"
    result = stack_arrays(loaded, feature_names)
    assert result.shape == (3, 6)
