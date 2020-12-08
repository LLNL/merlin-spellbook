###############################################################################
# Copyright (c) 2019, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory
# Written by the Merlin dev team, listed in the CONTRIBUTORS file.
# <merlin@llnl.gov>
#
# LLNL-CODE-797170
# All rights reserved.
# This file is part of merlin-spellbook.
#
# For details, see https://github.com/LLNL/merlin-spellbook and
# https://github.com/LLNL/merlin.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###############################################################################

import argparse
import sys

import numpy as np

from spellbook.utils import prep_argparse


try:
    import cPickle as pickle
except ImportError:
    import pickle


def setup_argparse(parent_parser=None, the_subparser=None):
    description = "Use a regressor to make a prediction"
    parser, subparsers = prep_argparse(description, parent_parser, the_subparser)

    # spellbook predict
    predict_parser = subparsers.add_parser(
        "predict",
        help=description,
    )
    predict_parser.set_defaults(func=predict)
    predict_parser.add_argument(
        "-infile", help=".npy file with data to predict", default="new_x.npy"
    )
    predict_parser.add_argument(
        "-reg", help="pickled regressor file", default="regressor.pkl"
    )
    predict_parser.add_argument(
        "-outfile", help="file to store the new predictions", default="new_y.npy"
    )

    return parser


def predict(args):
    regr = pickle.load(open(args.reg, "rb"))

    X = np.load(args.infile)

    new_y = regr.predict(X)
    np.save(open(args.outfile, "wb"), new_y)


def main():
    parser = setup_argparse()
    args = parser.parse_args()
    predict(args)


if __name__ == "__main__":
    sys.exit(main())
