import argparse


def prep_argparse(description, parent_parser=None, the_subparser=None):
    if parent_parser is None:
        parser = argparse.ArgumentParser(description=description)
        subparsers = parser.add_subparsers(dest="subparsers")
        subparsers.required = True
    else:
        parser = parent_parser
        subparsers = the_subparser
    return parser, subparsers
