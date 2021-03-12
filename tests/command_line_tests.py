###############################################################################
# Copyright (c) 2019, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory
# Written by the Merlin dev team, listed in the CONTRIBUTORS file.
# <merlin@llnl.gov>
#
# LLNL-CODE-797170
# All rights reserved.
# This file is part of Merlin Spellbook.
#
# For details, see https://github.com/LLNL/merlin.
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

"""
Script for running command line interface tests.
Built for 1) manual use and 2) continuous integration.
"""
import argparse
import os
import shutil
import sys
import time
from contextlib import suppress
from glob import glob
from re import search
from subprocess import PIPE, Popen


OUTPUT_DIR = "cli_test_studies"


def run_single_test(name, test, test_label="", buffer_length=50):
    dot_length = buffer_length - len(name) - len(str(test_label))
    print(f"TEST {test_label}: {name}{'.'*dot_length}", end="")
    command = test[0]
    conditions = test[1]
    if not isinstance(conditions, list):
        conditions = [conditions]

    start_time = time.time()
    process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    end_time = time.time()
    total_time = end_time - start_time
    if stdout is not None:
        stdout = stdout.decode("utf-8")
    if stderr is not None:
        stderr = stderr.decode("utf-8")
    return_code = process.returncode

    info = {
        "total_time": total_time,
        "command": command,
        "stdout": stdout,
        "stderr": stderr,
        "return_code": return_code,
    }

    # ensure all test conditions are satisfied
    for condition in conditions:
        condition.ingest_info(info)
        passed = condition.passes
        if passed is False:
            break

    return passed, info


def clear_test_studies_dir():
    """
    Deletes the 'test_studies' directory, in order to preserve
    state each time cli tests are run.
    """
    with suppress(FileNotFoundError):
        shutil.rmtree(f"./{OUTPUT_DIR}")


def process_test_result(passed, info, is_verbose, exit):
    """
    Process and print test results to the console.
    """
    # if the environment does not contain necessary programs, exit early.
    if passed is False and "spellbook: command not found" in info["stderr"]:
        print(f"\nMissing from environment:\n\t{info['stderr']}")
        return None
    elif passed is False:
        print("FAIL")
        if exit is True:
            return None
    else:
        print("pass")

    if is_verbose is True:
        print(f"\tcommand: {info['command']}")
        print(f"\telapsed time: {round(info['total_time'], 2)} s")
        if info["return_code"] != 0:
            print(f"\treturn code: {info['return_code']}")
        if info["stderr"] != "":
            print(f"\tstderr:\n{info['stderr']}")

    return passed


def run_tests(args, tests):
    """
    Run all inputted tests.
    :param `tests`: a dictionary of
        {"test_name" : ("test_command", [conditions])}
    """
    selective = False
    n_to_run = len(tests)
    if args.ids is not None and len(args.ids) > 0:
        if not all(x > 0 for x in args.ids):
            raise ValueError(f"Test ids must be between 1 and {len(tests)}, inclusive.")
        selective = True
        n_to_run = len(args.ids)

    print(f"Running {n_to_run} integration tests...")
    start_time = time.time()

    total = 0
    failures = 0
    for test_name, test in tests.items():
        test_label = total + 1
        if selective and test_label not in args.ids:
            total += 1
            continue
        try:
            passed, info = run_single_test(test_name, test, test_label)
        except BaseException as e:
            print(e)
            passed = False
            info = None

        result = process_test_result(passed, info, args.verbose, args.exit)
        if result is None:
            print("Exiting early")
            return 1
        if result is False:
            failures += 1
        total += 1

    end_time = time.time()
    total_time = end_time - start_time

    if failures == 0:
        print(f"Done. {n_to_run} tests passed in {round(total_time, 2)} s.")
        return 0
    print(
        f"Done. {failures} tests out of {n_to_run} failed after {round(total_time, 2)} s.\n"
    )
    return 1


class Condition:
    def ingest_info(self, info):
        """
        This function allows child classes of Condition
        to take in data AFTER a test is run.
        """
        for key, val in info.items():
            setattr(self, key, val)

    @property
    def passes(self):
        print("Extend this class!")
        return False


class ReturnCodeCond(Condition):
    """
    A condition that some process must return 0
    as its return code.
    """

    def __init__(self, expected_code=0):
        """
        :param `expected_code`: the expected return code
        """
        self.expected_code = expected_code

    @property
    def passes(self):
        return self.return_code == self.expected_code


class NoStderrCond(Condition):
    """
    A condition that some process have an empty
    stderr string.
    """

    @property
    def passes(self):
        return self.stderr == ""


class RegexCond(Condition):
    """
    A condition that some body of text MUST match a
    given regular expression. Defaults to stdout.
    """

    def __init__(self, regex, negate=False):
        """
        :param `regex`: a string regex pattern
        """
        self.regex = regex
        self.negate = negate

    def is_within(self, text):
        """
        :param `text`: text in which to search for a regex match
        """
        return search(self.regex, text) is not None

    @property
    def passes(self):
        if self.negate:
            return not self.is_within(self.stdout)
        return self.is_within(self.stdout) or self.is_within(self.stderr)


def define_tests():
    """
    Returns a dictionary of tests, where the key
    is the test's name, and the value is a tuple
    of (shell command, condition(s) to satisfy).
    """

    # shortcut string variables
    config_dir = "./CLI_TEST_MERLIN_CONFIG"

    return {
        "spellbook": ("spellbook", ReturnCodeCond(1)),
        "spellbook help": ("spellbook --help", ReturnCodeCond()),
        "spellbook version": ("spellbook --version", ReturnCodeCond()),
        "spellbook serialize": (
            "spellbook serialize --output thing.json --verbose --vars top/middle/bottom=1 top/middle/bottom2=2 top/middle/string=spam top/bool=false top/float=1.3e-9 top/1/junk=nan ; rm thing.json",
            RegexCond(
                '{"top": {"1": {"junk": NaN}, "bool": true, "float": 1.3e-09, "middle": {"bottom": 1, "bottom2": 2, "string": "spam"}}}'
            ),
        ),
        "spellbook make-samples": (
            "spellbook make-samples ; rm samples.npy",
            ReturnCodeCond(),
        ),
        # "spellbook learn": ("spellbook learn", ReturnCodeCond()),
        # "spellbook predict": ("spellbook predict", ReturnCodeCond()),
        # "spellbook collect": ("spellbook collect", ReturnCodeCond()),
        #    etc... lots of tests for each of these subcommands are needed.
        #    Make your own Condition classes and insert them after the command string.
    }


def setup_argparse():
    parser = argparse.ArgumentParser(description="run_tests cli parser")
    parser.add_argument(
        "--exit",
        action="store_true",
        help="Flag for stopping all testing upon first failure",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Flag for more detailed output messages"
    )
    parser.add_argument(
        "--ids",
        action="store",
        dest="ids",
        type=int,
        nargs="+",
        default=None,
        help="Provide space-delimited ids of tests you want to run."
        "Example: '--ids 1 5 8 13'",
    )
    return parser


def main():
    """
    High-level CLI test operations.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    tests = define_tests()

    clear_test_studies_dir()
    result = run_tests(args, tests)
    clear_test_studies_dir()
    return result


if __name__ == "__main__":
    sys.exit(main())
