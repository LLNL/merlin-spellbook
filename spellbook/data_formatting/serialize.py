#!/usr/bin/env python3
##############################################################################
# Copyright (c) Lawrence Livermore National Security, LLC and other
# Merlin-Spellbook Project developers. See top-level LICENSE and COPYRIGHT
# files for dates and other details. No copyright assignment is required to
# contribute to Merlin-Spellbook.
##############################################################################

import json


""" Serializes a command-line input variable list"""


def nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value


def convert_string(string):
    if string.lower() == "false":
        return False
    if string.lower() == "true":
        return True
    if string.isdigit():
        return int(string)
    try:
        return float(string)
    except ValueError:
        return string
    except OverflowError:
        return string


def nested_dict(var_list, splitter="/", delimiter="="):
    output = {}
    for v in var_list:
        keys, val = v.split(delimiter, 1)
        keylist = keys.split(splitter)
        value = convert_string(val)
        nested_set(output, keylist, value)
    return output


def parse_args(args):
    output = nested_dict(args.vars, splitter=args.splitter, delimiter=args.delimiter)
    dumpargs = {"sort_keys": True}
    if args.indent:
        dumpargs["indent"] = 4
    if args.verbose:
        print(json.dumps(output, **dumpargs))
    with open(args.output, "w") as f:
        json.dump(output, f, **dumpargs)
