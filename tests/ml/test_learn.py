import numpy as np

from merlin_spellbook.src.ml.learn import stack_arrays


def test_stack_arrays():
    data = np.random.random((3,2))
    # np.dump ... file.npz
    # data = np.load("file.npz")
    feature_names = "F1,F2,F3"
    result = stack_arrays(data, feature_names)
    print(result)
    assert result == result
