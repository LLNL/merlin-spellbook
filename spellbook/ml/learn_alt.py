import argparse
import sys

import numpy as np
from sklearn.ensemble import RandomForestRegressor


try:
    import cPickle as pickle
except ImportError:
    import pickle


FOREST_DEFAULTS = {"max_depth": 2, "random_state": 0, "n_estimators": 100}


def load_infile(args):
    with np.load(args.infile) as data:
        if args.X is not None:
            X = stack_arrays(data, args.X)  # inputs
        elif "X" in data.keys():
            X = data["X"]
        else:
            X = data[data.files[0]]

        if args.y is not None:
            y = stack_arrays(data, args.y)  # outputs
        elif "y" in data.keys():
            y = data["y"]
        else:
            y = data[data.files[1]]
    return X, y


def random_forest(args):
    forest_args = FOREST_DEFAULTS

    regr = RandomForestRegressor(**forest_args)
    X, y = load_infile(args)

    n_samples_X = X.shape[0]
    n_samples_y = y.shape[0]

    if n_samples_X != n_samples_y:
        raise ValueError("n_samples_X != n_samples_y")

    # single feature or sample reshape as appropriate for sklearn
    if n_samples_y == 1:
        y.reshape((1, -1))
    elif len(y.shape) == 1:
        y.reshape((-1, 1))

    regr.fit(X, y)
    with open(args.outfile, "wb") as f:
        pickle.dump(regr, f)


def stack_arrays(data, delimited_names, delimiter=","):
    stacked = np.vstack([data[name] for name in delimited_names.split(delimiter)])
    return stacked.T
