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
from maestrowf.datastructures.core import ParameterGenerator

from merlin.common.util_sampling import scale_samples


def setup_argparse():
    parser = argparse.ArgumentParser('Generate some samples!')
    parser.add_argument('-n', help='number of samples', default=100, type=int)
    parser.add_argument('-dims', help='number of dimensions', default=2, type=int)
    parser.add_argument('-sample_type',
    help='type of sampling. options: random, grid. If grid, will try to get close to the correct number of samples',
    default='random')
    parser.add_argument('-outfile', help='name of output .npy file',
                    default='samples')
    parser.add_argument(
        '-scale',
        help='ranges to scale results in form "[(min,max,type),(min,max,type)]" where type = "linear" or "log"')
    return parser


def process_args(args):
    n_samples = args.n
    n_dims = args.dims
    sample_type = args.sample_type

    if args.scale is not None:
        scales = eval(args.scale)
    else:
        scales = n_dims * [(0, 1, 'linear')]

    limits = []
    do_log = []
    for scale in scales:
        limits.append((scale[0], scale[1]))
        if scale[2] == 'log':
            do_log.append(True)
        else:
            do_log.append(False)

    if sample_type == 'random':
        x = np.random.random((n_samples, n_dims))
    elif sample_type == 'grid':
        subdivision = int(pow(n_samples, 1 / float(n_dims)))
        temp = [np.linspace(0, 1.0, subdivision) for i in range(n_dims)]
        X = np.meshgrid(*temp)
        x = np.stack([xx.flatten() for xx in X], axis=1)

    x = scale_samples(x, limits, do_log=do_log)

    np.save(args.outfile, x)


def main():
    parser = setup_argparse()
    args = parser.parse_args()   
    process_args(args)


if __name__ == "__main__":
    sys.exit(main())

