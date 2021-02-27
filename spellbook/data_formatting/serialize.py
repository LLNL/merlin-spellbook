#!/usr/bin/env python3

import json
import os
import sys


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


def parse_args(args):
    output = nested_dict(args.vars, splitter=args.splitter)
    dumpargs = {"sort_keys": True}
    if args.indent:
        dumpargs["indent"] = 4
    if args.verbose:
        print(json.dumps(output, **dumpargs))
    with open(args.output, "w") as f:
        json.dump(output, f, **dumpargs)
