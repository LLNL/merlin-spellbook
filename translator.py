import argparse
import sys
import os

import numpy as np

import conduit
import conduit_bundler as cb


def setup_argparse():
    parser = argparse.ArgumentParser(
        description='Translate a flat sample file into another format (conduit-compatible or numpy)", filtering with an external schema.')

    parser.add_argument('-input', help='.hdf5 file with data in it',
                    default='results_features.hdf5')
    parser.add_argument('-output', help='.npz file with the arrays',
                    default='results_features.npz')
    parser.add_argument(
    '-schema',
    help='schema for a single sample that says what data to translate',
    default='features_translate.json')
    return parser


def process_args(args):
    data = cb.load_node(args.input)
    with open(args.schema, 'r') as f:
        schema_json = f.read()

    g = conduit.Generator(schema_json, 'json')
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
    if protocol == 'npz':
        np.savez(args.output, **all_dict)
    else:
        n = conduit.Node()
        g.walk_external(n)
        n.update_compatible(data)
        for data_name in all_dict.keys():
            n[data_name] = np.array(all_dict[data_name])
        cb.dump_node(n, args.output)


def generate_scalar_path_pairs(node, path=""):
    """ Walk through the node finding the paths to the data and the data """
    children = node.child_names()
    for child in children:
        if isinstance(node[child], conduit.Node):
            for pair in generate_scalar_path_pairs(
                    node[child], path=os.path.join(os.path.join(path, child), ''):
                yield pair
        else:
            yield os.path.join(path, child), node[child]


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


