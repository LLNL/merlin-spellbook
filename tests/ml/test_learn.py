import os

import numpy as np

from spellbook.ml.learn import stack_arrays


def test_stack_arrays():
    data1 = np.random.random((3, 2))
    data2 = np.zeros((3, 2))
    data3 = np.ones((3, 2))
    np.savez("temp.npz", F1=data1, F2=data2, F3=data3)
    loaded = np.load("temp.npz")
    os.remove("temp.npz")
    feature_names = "F1,F2,F3"
    result = stack_arrays(loaded, feature_names)
    assert result.shape == (2, 9)
