#!/usr/bin/env python3

import argparse
import os
import sys

import numpy as np

from spellbook.utils import prep_argparse


""" Merges npz files. See https://jiafulow.github.io/blog/2019/02/17/merge-arrays-from-multiple-npz-files/"""


class Stacker(object):
    def __init__(self):
        self.d = {}
        self.dout = {}

    def run(self, target, source, force=False):
        print("hadd Target file: {0}".format(target))

        if not force:
            if os.path.isfile(target):
                print(
                    "stack_npz error opening target file (does {0} exist?).".format(
                        target
                    )
                )
                print('Pass "-f" argument to force re-creation of output file.')

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
            vv = np.hstack(v)
            self.dout[k] = vv

        # Write to the target file
        np.savez_compressed(target, **self.dout)
        print("DONE")


def process_args(args):
    stacker = Stacker()
    stacker.run(args.target, args.source, force=args.force)


def setup_argparse(parent_parser=None, the_subparser=None):
    description = "stacker for npz files."
    parser, subparsers = prep_argparse(description, parent_parser, the_subparser)

    # spellbook stack-npz
    stack_npz = subparsers.add_parser(
        "stack-npz",
        help=description,
    )
    stack_npz.set_defaults(func=process_args)
    stack_npz.add_argument(
        "-f", "--force", action="store_true", help="Force write the target file"
    )
    stack_npz.add_argument("target", help="target file")
    stack_npz.add_argument("source", nargs="+", help="source files")
    return parser


def main():
    parser = setup_argparse()
    args = parser.parse_args()
    process_args(args)


if __name__ == "__main__":
    sys.exit(main())
