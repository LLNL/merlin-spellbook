#!/usr/bin/env python3
##############################################################################
# Copyright (c) Lawrence Livermore National Security, LLC and other
# Merlin-Spellbook Project developers. See top-level LICENSE and COPYRIGHT
# files for dates and other details. No copyright assignment is required to
# contribute to Merlin-Spellbook.
##############################################################################

import os
import shutil

import numpy as np


""" Merges npz files. Modified from https://jiafulow.github.io/blog/2019/02/17/merge-arrays-from-multiple-npz-files/"""


def find_max_dims(arrays):
    dims = np.atleast_2d(arrays[0]).shape
    for a in arrays[1:]:
        dims = np.max((dims, np.atleast_2d(a).shape), axis=0)
    return dims


def pad_many(arrays, dims, dont_pad_first=False, value=np.nan):
    fixed = []
    zeros = np.zeros_like(dims)
    for a in arrays:
        pad_dist = dims - np.atleast_2d(a).shape
        if dont_pad_first:
            pad_dist[0] = 0
        padder = np.column_stack((zeros, pad_dist))
        fixed.append(np.pad(np.atleast_2d(a), padder, mode="constant", constant_values=value))
    return fixed


def stack_jagged(arrays, dont_pad_first=True, stack_func=np.vstack, **kwargs):
    dims = find_max_dims(arrays)
    padded = pad_many(arrays, dims, dont_pad_first, **kwargs)
    result = stack_func(padded)
    return result


class Stacker(object):
    def __init__(self):
        self.d = {}
        self.dout = {}

    def run(self, target, source, force=False):

        print("Target file: {0}".format(target))

        if not force:
            if os.path.isfile(target):
                print("stack_npz error opening target file (does {0} exist?).".format(target))
                print('Pass "-f" argument to force re-creation of output file.')
                return

        n_source = len(source)
        if n_source == 1:
            print("Only one source file given! Not stacking, just doing a copy.")
            shutil.copy(source[0], target)
            print("DONE")
            return

        # Loop over the source files
        for i, s in enumerate(source):
            print("stack_npz Source file {0}: {1}".format(i, s))
            with np.load(s) as data:
                if i == 0:
                    for k in data.files:
                        self.d[k] = []
                # Loop over all the keys
                for k in data.files:
                    self.d[k].append(data[k])

        # Merge arrays via np.hstack()
        print("stacking...")
        for k, v in self.d.items():
            try:
                vv = stack_jagged(v)
                self.dout[k] = vv
            except Exception:
                print(f"Error stacking {k}")

        # Write to the target file
        np.savez_compressed(target, **self.dout)
        print("DONE")


def process_args(args):
    stacker = Stacker()
    stacker.run(args.target, args.source, force=args.force)
