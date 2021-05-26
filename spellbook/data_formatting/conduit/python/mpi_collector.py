import os
import pickle as pkl
import sys
from uuid import uuid4

from spellbook.data_formatting.conduit.python import conduit_bundler as cb


WARN = ""
try:
    import conduit
except:
    WARN = "\nWARNING: conduit not found."
NAME = os.path.basename(__file__)


def savename(file_no, outfile):
    base, ext = outfile.split(".")
    name = f"{base}_{file_no:03}.{ext}"
    return name


def make_schema_compatible(original_node, add_uuid):
    node = conduit.Node()
    if add_uuid:
        node[str(uuid4())] = original_node
    else:
        node = original_node
    return node


def process_args(args):
    n_chunks = MPI.COMM_WORLD.Get_size()
    my_rank = MPI.COMM_WORLD.Get_rank()
    filepath_chunks = pkl.load(open(args.filepath_chunks, "rb"))
    my_filepaths = filepath_chunks[my_rank]
    chunk = conduit.Node()
    results = []
    for path in my_filepaths:
        # TODO: logger.DEBUG print(f'{my_rank} trying {path}')
        if not path or path == "":
            print(f'{my_rank} error with path {path}')
            continue
        try:
            subnode = cb.load_node(path)
            # TODO: logger.DEBUG print(f'{my_rank} loaded {path}')
            # TODO: logger.DEBUG print(f'{my_rank}: {subnode.child_names()}')
            subnode = make_schema_compatible(subnode, args.add_uuid)
            for top_path in subnode.child_names():
                if top_path in results:
                    # TODO: logger.DEBUG print(f"Error! Already in results: {top_path}")
                    new_path = "-".join((top_path, str(uuid4())))
                    # TODO: logger.DEBUG print(f"Renaming duplicate to node to: {new_path}")
                else:
                    new_path = top_path
                # TODO: logger.DEBUG print(f'{my_rank}: {top_path} --> {new_path}')
                chunk[new_path] = subnode[top_path]
                results.append(top_path)
        except:
            print(f"'{NAME}' unable to load '{path}'!")
    cb.dump_node(chunk, savename(my_rank, args.outfile))
