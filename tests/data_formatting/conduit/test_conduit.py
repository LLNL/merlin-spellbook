import os
import sys

import numpy as np



try:
    import conduit
    from spellbook.data_formatting.conduit.python import conduit_bundler as cb
except ModuleNotFoundError:
    print("Conduit not available! These tests will fail!")
    cb = None

def make_dummy_node():
    x = conduit.Node()
    data_types = [1, 1.0, "hi", "c"]
    for d in data_types:
        key = str(type(d))
        x[key] = d
    return x


def test_make_conduit_node():
    x = make_dummy_node()


def test_save_node():
    x = make_dummy_node()
    save_node_many(x)
    delete_data()


def save_node_many(
    node, base="_dummy", exts=(".h5", ".hdf5", ".json", ".yaml", ".cbin")
):
    for ext in exts:
        cb.dump_node(node, base + ext)


def delete_conduit_file(filename):
    protocol = cb.determine_protocol(filename)
    if protocol == "cbin":
        os.remove(filename + "_json")
    os.remove(filename)


def test_load_node():
    x = make_dummy_node()
    save_node_many(x)
    _ = load_node_many(base="_dummy")
    delete_data()


def test_load_handle():
    base = "_dummy"
    exts = (".h5", ".hdf5", ".json", ".yaml", ".cbin")
    x = make_dummy_node()
    y = conduit.Node()
    y["x"] = x
    y["z"] = "z"
    save_node_many(y, base=base, exts=exts)
    just_handles = load_node_many(base=base, exts=exts, path=None)
    just_x = load_node_many(base=base, exts=exts, path="x")
    bad_path1 = load_node_many(base=base, exts=exts, path="bogus")
    bad_path2 = load_node_many(base=base, exts=exts, path="")
    all_data = load_node_many(base=base, exts=exts, path="/")
    for h in just_handles:
        assert h.has_path("x")
        assert h.has_path("z")
        h.close()
    for h in just_x:
        assert nodes_equal(h, x)
    for h in bad_path1:
        assert h is None
    for h in bad_path2:
        assert h is None
    for h in all_data:
        assert nodes_equal(h, y)
    delete_data(base=base, exts=exts)


def delete_data(base="_dummy", exts=(".h5", ".hdf5", ".json", ".yaml", ".cbin")):
    for ext in exts:
        delete_conduit_file(base + ext)


def nodes_equal(node1, node2):
    return node1.to_json() == node2.to_json()


def load_node_many(
    base="_dummy", exts=(".h5", ".hdf5", ".json", ".yaml", ".cbin"), path="/"
):
    nodes = []
    for ext in exts:
        node = cb.load_node(base + ext, path)
        nodes.append(node)
    return nodes
