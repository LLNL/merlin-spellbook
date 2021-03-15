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

import sys

import numpy as np

from spellbook.data_formatting.conduit.python import conduit_bundler as cb


WARN = ""
try:
    import conduit
    import conduit.relay.io
except:
    WARN = "\nWARNING: conduit not found."


def process_args(args):
    print(WARN)
    protocol = cb.determine_protocol(args.output)
    # Faster loader, just read metadata
    data_loader = cb.load_node_handle(args.input)
    first_data = conduit.Node()
    data_loader.read(first_data, data_loader.list_child_names()[0])
    if args.schema == "auto":
        schema_json = first_data.to_json()
    elif "," in args.schema:
        sub_list = args.schema.split(",")
        schema_node = conduit.Node()
        for item in sub_list:
            schema_node[item] = first_data[item]
        schema_json = schema_node.to_json()
    else:
        with open(args.schema, "r") as f:
            schema_json = f.read()

    g = conduit.Generator(schema_json, "json")
    schema = conduit.Node()
    g.walk_external(schema)

    data_paths = []
    for path, _ in generate_scalar_path_pairs(schema):
        data_paths.append(path)
    samples = data_loader.list_child_names()

    # Walk through all the samples and create a unified list (ie pack into a
    # dictionary of lists)
    all_dict = {}
    for s in samples:
        filtered_node = conduit.Node()
        for path in data_paths:
            sample_path = "/".join((s, path))
            if data_loader.has_path(sample_path):
                data_loader.read(filtered_node[path], sample_path)
            else:
                filtered_node[
                    sample_path
                ] = np.nan  # if a value is missing, that could be a problem
        make_data_array_dict(all_dict, filtered_node)

    for dat in all_dict.keys():
        all_dict[dat] = np.vstack(all_dict[dat])
    # Save according to output extension, either numpy or conduit-compatible
    if protocol == "npz":
        np.savez(args.output, **all_dict)
    else:
        n = cb.pack_conduit_node_from_dict(all_dict)
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
        # patch for older versions of conduit
        datum = np.array(datum)
        if path in d:
            d[path].append(datum)
        else:
            d[path] = [datum]
