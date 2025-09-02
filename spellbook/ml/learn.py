##############################################################################
# Copyright (c) Lawrence Livermore National Security, LLC and other
# Merlin-Spellbook Project developers. See top-level LICENSE and COPYRIGHT
# files for dates and other details. No copyright assignment is required to
# contribute to Merlin-Spellbook.
##############################################################################

import spellbook.ml.surrogates as surrogates
from spellbook.utils import load_infile


try:
    import cPickle as pickle
except ImportError:
    import pickle


def make_regressor(args):
    if args.reg_args is None:
        reg_args = {}
    else:
        reg_args = args.reg_args

    regr = surrogates.sklearnRegressors.factory(args.regressor, **reg_args)
    X, y = load_infile(args.infile, X_keys=args.X, y_keys=args.y)

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
