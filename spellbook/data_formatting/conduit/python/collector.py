from __future__ import print_function

import argparse
import json
import sys
from uuid import uuid4

from spellbook.utils import prep_argparse


def import_conduit():
    import conduit
    import conduit_bundler as cb


def process_args(args):
    import_conduit()
    result = conduit.Node()
    results = []
    for path in args.infiles.split():
        try:
            subnode = cb.load_node(path)
            for top_path in subnode.child_names():

                if top_path in results:
                    print("Error! Already in results: " + top_path)
                    top_path = "-".join((top_path, uuid4()))
                    print("Renaming duplicate to node to: " + top_path)

                result[top_path] = subnode[top_path]
                results.append(top_path)
        except:
            print("Unable to load " + path)

    cb.dump_node(result, args.outfile)


def setup_argparse(parent_parser=None, the_subparser=None):
    description = "Convert a list of conduit-readable files into a single big conduit node. Simple append, so nodes that already exist will get a name change to conflict-uuid"
    parser, subparsers = prep_argparse(description, parent_parser, the_subparser)

    # spellbook collect
    collect = subparsers.add_parser(
        "collect",
        help=description,
    )
    collect.set_defaults(func=process_args)
    collect.add_argument(
        "-infiles", help="whitespace separated list of files to collect", default=""
    )
    collect.add_argument("-outfile", help="aggregated file", default="results.hdf5")
    return parser


def main():
    parser = setup_argparse()
    args = parser.parse_args()
    process_args(args)


if __name__ == "__main__":
    sys.exit(main())
