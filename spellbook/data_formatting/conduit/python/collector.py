from __future__ import print_function

import argparse
import json
import sys
from itertools import zip_longest
from uuid import uuid4

from spellbook.data_formatting.conduit.python import conduit_bundler as cb
from spellbook.utils import prep_argparse


WARN = ""
try:
    import conduit
except:
    WARN = "\nWARNING: conduit not found."


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=None)


def savename(file_no, args):
    if args.chunk_size:
        base, ext = args.outfile.split(".")
        name = f"{base}_{file_no:03}.{ext}"
        return name
    return args.outfile


def process_args(args):

    files = args.infiles
    nfiles = len(files)
    if not args.chunk_size:
        chunk_size = nfiles
    else:
        chunk_size = args.chunk_size

    fileno = 0
    results = []
    for group in grouper(files, chunk_size):
        result = conduit.Node()
        for path in group:
            if not path:
                continue
            try:
                subnode = cb.load_node(path)
                for top_path in subnode.child_names():

                    if top_path in results:
                        print("Error! Already in results: " + top_path)
                        new_path = "-".join((top_path, str(uuid4())))
                        print("Renaming duplicate to node to: " + new_path)
                    else:
                        new_path = top_path

                    result[new_path] = subnode[top_path]
                    results.append(top_path)
            except:
                print("Unable to load " + path)

        cb.dump_node(result, savename(fileno, args))
        fileno = fileno + 1


def setup_argparse(parent_parser=None, the_subparser=None):
    description = "Convert a list of conduit-readable files into a single big conduit node. Simple append, so nodes that already exist will get a name change to conflict-uuid{}".format(
        WARN
    )
    parser, subparsers = prep_argparse(description, parent_parser, the_subparser)

    # spellbook collect
    collect = subparsers.add_parser("collect", help=description)
    collect.set_defaults(func=process_args)
    collect.add_argument(
        "-infiles",
        help="whitespace separated list of files to collect",
        default="",
        nargs="+",
    )
    collect.add_argument(
        "-outfile",
        help="aggregated file root. If chunking will insert _n before extension",
        default="results.hdf5",
    )
    collect.add_argument(
        "-chunk_size",
        help="number of files to chunk together. Default (None): don't chunk",
        default=None,
        type=int,
    )
    return parser


def main():
    parser = setup_argparse()
    args = parser.parse_args()
    process_args(args)


if __name__ == "__main__":
    sys.exit(main())
