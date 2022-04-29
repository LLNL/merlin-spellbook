###############################################################################
# Copyright (c) 2022, Lawrence Livermore National Security, LLC.
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
import shutil
import subprocess
import sys
import time
from contextlib import suppress
from re import search
from subprocess import PIPE
from typing import Any, Dict, Tuple


OUTPUT_DIR = "cli_test_studies"


def run_single_test(test_name: str, test: tuple, test_id: int, buffer_length: int = 50) -> Tuple[bool, dict]:
    """Run a single test

    Args:
        test_name (str): Test name
        test (tuple): Test
        test_id (int): Test id corresponding to test name
        buffer_length (int, optional): _description_. Defaults to 50.

    Returns:
        Tuple[bool, dict]: _description_
    """
    print(f"TEST {test_id}: {test_name:{'.'}<{buffer_length}}", end="")
    command = test[0]
    conditions = test[1] if isinstance(test[1], list) else [test[1]]

    start_time = time.time()
    process = subprocess.run(command, stdout=PIPE, stderr=PIPE, shell=True)
    end_time = time.time()
    total_time = end_time - start_time

    if process.stdout is not None:
        stdout = process.stdout.decode("utf-8")
    if process.stderr is not None:
        stderr = process.stderr.decode("utf-8")

    info = {
        "total_time": total_time,
        "command": command,
        "stdout": stdout,
        "stderr": stderr,
        "return_code": process.returncode,
    }

    # ensure all test conditions are satisfied
    passed: bool
    for condition in conditions:
        condition.ingest_info(info)
        passed = condition.passes
        if passed is False:
            break

    return passed, info


def clear_test_studies_dir() -> None:
    """
    Deletes the 'test_studies' directory, in order to preserve
    state each time cli tests are run.
    """
    with suppress(FileNotFoundError):
        shutil.rmtree(f"./{OUTPUT_DIR}")


def process_test_result(passed: bool, info: dict, is_verbose: bool, early_exit: bool) -> int:
    """Process and print test results to the console.

    Args:
        passed (bool): Flag describing whether the tests passed
        info (dict): Information about the tests ran
        is_verbose (bool): Verbose
        early_exit (bool): Early early_exit

    Returns:
        int: exit status: -1 is exit, 0 is failed, 1 is passed
    """
    # if the environment does not contain necessary programs, exit early.
    if passed is False and "spellbook: command not found" in info["stderr"]:
        print(f"\nMissing from environment:\n\t{info['stderr']}")
        return -1
    if passed is False:
        print("FAIL")
        if early_exit:
            return -1
    else:
        print("PASS")

    if is_verbose:
        print(f"\tcommand: {info['command']}")
        print(f"\telapsed time: {round(info['total_time'], 2)} s")
        if info["return_code"] != 0:
            print(f"\treturn code: {info['return_code']}")
        if info["stderr"] != "":
            print(f"\tstderr:\n{info['stderr']}")

    return 1 if passed else 0


def run_tests(args: argparse.Namespace, tests: Dict[str, tuple]) -> int:
    """
     Run all defined tests or only ones specified by args

    Args:
        args (argparse.Namespace): Parsed arguments
        tests (Dict[str, tuple]): {"test_name" : ("test_command", [conditions])}

    Returns:
        int: 0 for success, 1 for fail
    """
    if args.ids is None:
        test_ids = list(range(1, len(tests) + 1))
    elif sum(0 < test_id <= len(tests) for test_id in args.ids) == len(args.ids):
        test_ids = args.ids
    else:
        raise ValueError(f"Test ids must be between 1 and {len(tests)}, inclusive.")

    print(f"Running {len(test_ids)} integration tests...")
    start_time = time.time()

    failures = 0
    for label_id, (test_name, test) in enumerate(tests.items(), 1):
        if label_id not in test_ids:
            continue
        try:
            passed, info = run_single_test(test_name, test, label_id)
        except BaseException as err:
            print(err)
            raise BaseException("Sorry, not quiet sure what happened") from err

        result = process_test_result(passed, info, args.verbose, args.early_exit)
        if result == -1:
            print("Exiting early")
            return 1

        failures += not passed

    end_time = time.time()
    total_time = end_time - start_time

    if failures == 0:
        print(f"Done. {len(test_ids)} tests passed in {round(total_time, 2)} s.")
        return 0
    print(f"Done. {failures} tests out of {len(test_ids)} failed after {round(total_time, 2)} s.\n")
    return 1


class Condition:
    def ingest_info(self, info: Dict[str, Any]) -> None:
        """
        This function allows child classes of Condition
        to take in data AFTER a test is run.
        """
        for key, val in info.items():
            setattr(self, key, val)

    @property
    def passes(self) -> bool:
        print("Extend this class!")
        return False


class ReturnCodeCond(Condition):
    """
    A condition that some process must return 0
    as its return code.
    """

    def __init__(self, expected_code: int = 0) -> None:
        """
        :param `expected_code`: the expected return code
        """
        self.expected_code = expected_code

    @property
    def passes(self) -> bool:
        return self.return_code == self.expected_code


class NoStderrCond(Condition):
    """
    A condition that some process have an empty
    stderr string.
    """

    @property
    def passes(self) -> bool:
        return self.stderr == ""


class RegexCond(Condition):
    """
    A condition that some body of text MUST match a
    given regular expression. Defaults to stdout.
    """

    def __init__(self, regex: str, negate: bool = False) -> None:
        """

        Args:
            regex (str): a string regex pattern
            negate (bool, optional): negate the search result. Defaults to False.
        """
        self.regex = regex
        self.negate = negate

    def is_within(self, text: str) -> bool:
        """Searches for self.regex in text

        Args:
            text (str): text in which to search for a regex match

        Returns:
            bool: returns True if there was a match, False otherwise
        """
        return search(self.regex, text) is not None

    @property
    def passes(self) -> bool:
        if self.negate:
            return not self.is_within(self.stdout)
        return self.is_within(self.stdout) or self.is_within(self.stderr)


def define_tests() -> Dict[str, tuple]:
    """
    Returns a dictionary of tests, where the key
    is the test's name, and the value is a tuple
    of (shell command, condition(s) to satisfy).
    """

    # shortcut string variables
    # config_dir = "./CLI_TEST_MERLIN_CONFIG"

    return {
        "spellbook": ("spellbook", ReturnCodeCond(1)),
        "spellbook help": ("spellbook --help", ReturnCodeCond()),
        "spellbook version": ("spellbook --version", ReturnCodeCond()),
        "spellbook serialize": (
            "spellbook serialize --output thing.json --verbose --vars top/middle/bottom=1 top/middle/bottom2=2 top/middle/string=spam top/bool=false top/float=1.3e-9 top/1/junk=nan ; rm thing.json",
            RegexCond(
                '{"top": {"1": {"junk": NaN}, "bool": false, "float": 1.3e-09, "middle": {"bottom": 1, "bottom2": 2, "string": "spam"}}}'
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


def setup_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="run_tests cli parser")
    parser.add_argument(
        "--early_exit",
        action="store_true",
        help="Flag for stopping all testing upon first failure",
    )
    parser.add_argument("--verbose", action="store_true", help="Flag for more detailed output messages")
    parser.add_argument(
        "--ids",
        action="store",
        dest="ids",
        type=int,
        nargs="+",
        default=None,
        help="Provide space-delimited ids of tests you want to run." "Example: '--ids 1 5 8 13'",
    )
    return parser


def main() -> int:
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
