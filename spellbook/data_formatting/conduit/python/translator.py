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


def import_conduit():
    import conduit
    import conduit_bundler as cb


def setup_argparse(parent_parser=None, the_subparser=None):
    description = 'Flatten sample file into another format (conduit-compatible or numpy)", filtering with an external schema.'
    parser, subparsers = prep_argparse(description, parent_parser, the_subparser)

    # spellbook translate
    translate = subparsers.add_parser(
        "translate",
        help=description,
    )
    translate.set_defaults(func=process_args)
    translate.add_argument(
        "-input", help=".hdf5 file with data in it", default="results_features.hdf5"
    )
    translate.add_argument(
        "-output", help=".npz file with the arrays", default="results_features.npz"
    )
    translate.add_argument(
        "-schema",
        help="schema for a single sample that says what data to translate. Defaults to whole first node. Can be a comma-delimited list of subpaths, eg inputs,outputs/scalars,metadata",
        default="auto",
    )
    return translate


def process_args(args):
    import_conduit()
    data = cb.load_node(args.input)
    if args.schema == "auto":
        schema_json = data[data.child_names()[0]].to_json()
    elif "," in args.schema:
        sub_list = args.schema.split(",")
        schema_node = conduit.Node()
        for item in sub_list:
            schema_node[item] = data[data.child_names()[0] + "/" + item]
        schema_json = schema_node.to_json()
        print(schema_json)
    else:
        with open(args.schema, "r") as f:
            schema_json = f.read()

    g = conduit.Generator(schema_json, "json")
    schema = conduit.Node()
    g.walk_external(schema)

    samples = data.child_names()

    # Walk through all the samples and create a unified list (ie pack into a
    # dictionary of lists)
    all_dict = {}
    for s in samples:
        unfiltered_node = data[s]
        filtered_node = conduit.Node()
        g.walk_external(filtered_node)
        filtered_node.update_compatible(unfiltered_node)
        make_data_array_dict(all_dict, filtered_node)

    # Save according to output extension, either numpy or conduit-compatible
    protocol = cb.determine_protocol(args.output)
    if protocol == "npz":
        np.savez(args.output, **all_dict)
    else:
        n = cb.pack_conduit_node_from_dict(all_dict)
        # n = conduit.Node()
        # g.walk_external(n)
        # n.update_compatible(data)
        # for data_name in all_dict.keys():
        #    n[data_name] = np.array(all_dict[data_name]).
        cb.dump_node(n, args.output)


def generate_scalar_path_pairs(node, path=""):
    """ Walk through the node finding the paths to the data and the data """
    children = node.child_names()
    for child in children:
        if isinstance(node[child], conduit.Node):
            for pair in generate_scalar_path_pairs(
                node[child], path=path + child + "/"
            ):
                yield pair
        else:
            yield path + child, node[child]


def make_data_array_dict(d, node):
    """ Pact a node to the end of the list in the dictionary with same name path """
    for path, datum in generate_scalar_path_pairs(node):
        if path in d:
            d[path].append(datum)
        else:
            d[path] = [datum]


def main():
    parser = setup_argparse()
    args = parser.parse_args()
    process_args(args)


if __name__ == "__main__":
    sys.exit(main())
