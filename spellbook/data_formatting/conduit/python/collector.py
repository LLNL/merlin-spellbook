##############################################################################
# Copyright (c) Lawrence Livermore National Security, LLC and other
# Merlin-Spellbook Project developers. See top-level LICENSE and COPYRIGHT
# files for dates and other details. No copyright assignment is required to
# contribute to Merlin-Spellbook.
##############################################################################

from __future__ import print_function

from itertools import zip_longest
from uuid import uuid4

from spellbook.data_formatting.conduit.python import conduit_bundler as cb


WARN = ""
try:
    import conduit
except ModuleNotFoundError:
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


def make_schema_compatible(original_node, add_uuid):
    node = conduit.Node()
    if add_uuid:
        node[str(uuid4())] = original_node
    else:
        node = original_node
    return node


def process_args(args):
    print(WARN)
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
                subnode = make_schema_compatible(subnode, args.add_uuid)
                for top_path in subnode.child_names():

                    if top_path in results:
                        print("Error! Already in results: " + top_path)
                        new_path = "-".join((top_path, str(uuid4())))
                        print("Renaming duplicate to node to: " + new_path)
                    else:
                        new_path = top_path

                    result[new_path] = subnode[top_path]
                    results.append(top_path)
            except IOError:
                print("Unable to load " + path)

        cb.dump_node(result, savename(fileno, args))
        fileno = fileno + 1
