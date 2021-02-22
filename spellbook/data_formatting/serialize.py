#!/usr/bin/env python3

import argparse
import json
import os
import sys

from spellbook.utils import prep_argparse


""" Serializes a command-line input variable list"""


def nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value


def maybe_numeric_or_bool(string):
    if string.lower() == "false" or string.lower() == "true":
        return bool(string)
    if string.isdigit():
        return int(string)
    try:
        return float(string)
    except:
        return string


def nested_dict(var_list, splitter="/"):
    output = {}
    for v in var_list:
        keys, val = v.split("=")
        keylist = keys.split(splitter)
        value = maybe_numeric_or_bool(val)
        nested_set(output, keylist, value)
    return output


def process_args(args):
    output = nested_dict(args.vars, splitter=args.splitter)
    dumpargs = {"sort_keys": True}
    if args.indent:
        dumpargs["indent"] = 4
    if args.verbose:
        print(json.dumps(output, **dumpargs))
    with open(args.output, "w") as f:
        json.dump(output, f, **dumpargs)


def setup_argparse(parent_parser=None, the_subparser=None):
    description = "write a serialized file from cli arguments."
    parser, subparsers = prep_argparse(description, parent_parser, the_subparser)

    # spellbook stack-npz
    serialize = subparsers.add_parser(
        "serialize",
        help=description,
    )
    serialize.set_defaults(func=process_args)
    serialize.add_argument("--output", help="output file", default="output.json")
    serialize.add_argument(
        "--vars",
        nargs="+",
        help="variables to write. specified as space separated name=VALUE",
    )
    serialize.add_argument(
        "--splitter", help="key to indicate a nested value, default: /", default="/"
    )
    serialize.add_argument(
        "--verbose",
        help="print output, default False",
        action="store_true",
        default=False,
    )
    serialize.add_argument(
        "--indent",
        help="indent with new lines, default False",
        action="store_true",
        default=False,
    )
    return parser


def main():
    parser = setup_argparse()
    args = parser.parse_args()
    process_args(args)


if __name__ == "__main__":
    sys.exit(main())
