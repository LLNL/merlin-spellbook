##############################################################################
# Copyright (c) Lawrence Livermore National Security, LLC and other
# Merlin-Spellbook Project developers. See top-level LICENSE and COPYRIGHT
# files for dates and other details. No copyright assignment is required to
# contribute to Merlin-Spellbook.
##############################################################################

import numpy as np


try:
    import cPickle as pickle
except ImportError:
    import pickle


def predict(args):
    regr = pickle.load(open(args.reg, "rb"))

    X = np.load(args.infile)

    new_y = regr.predict(X)
    np.save(open(args.outfile, "wb"), new_y)
