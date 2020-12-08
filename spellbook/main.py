import glob
import logging
import os
import sys
import time
import traceback
from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    RawDescriptionHelpFormatter,
    RawTextHelpFormatter,
)
from contextlib import suppress

from spellbook import VERSION
from spellbook.data_formatting import stack_npz
from spellbook.data_formatting.conduit.python import collector, translator
from spellbook.ml import learn, predict, surrogates
from spellbook.sampling import make_samples


class HelpParser(ArgumentParser):
    """This class overrides the error message of the argument parser to
    print the help message when an error happens."""

    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


def setup_argparse():
    """
    Setup argparse and any CLI options we want available via the package.
    """
    parser = HelpParser(
        prog="spellbook",
        description="Merlin Spellbook -- scientific workflow utilities",
        formatter_class=RawDescriptionHelpFormatter,
        epilog="See spellbook <command> --help for more info",
    )
    parser.add_argument("-v", "--version", action="version", version=VERSION)
    subparsers = parser.add_subparsers(dest="subparsers")
    subparsers.required = True

    # spellbook make-samples
    make_samples.setup_argparse(parser, subparsers)

    # spellbook learn
    learn.setup_argparse(parser, subparsers)

    # spellbook predict
    predict.setup_argparse(parser, subparsers)

    # spellbook surrogates
    # surrogates.setup_argparse(parser, subparsers) TODO set up surrogates script?

    # spellbook collect
    collector.setup_argparse(parser, subparsers)

    # spellbook translate
    translator.setup_argparse(parser, subparsers)

    # spellbook stack-npz
    stack_npz.setup_argparse(parser, subparsers)

    return parser


def main():
    """
    High-level CLI operations.
    """
    parser = setup_argparse()
    if len(sys.argv) == 1:
        parser.print_help(sys.stdout)
        return 1
    args = parser.parse_args()

    try:
        args.func(args)
    except Exception as e:
        print(str(e))
        return 1


if __name__ == "__main__":
    sys.exit(main())
