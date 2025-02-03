#!/usr/bin/env python

import shutil
import sys
from pathlib import Path
from platform import python_implementation, python_version

from robot import rebot, run
from robot.api import ExecutionResult, ResultVisitor

CURDIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURDIR.parent))

from robot.version import VERSION  # noqa

from robotstatuschecker import process_output  # noqa


def check_tests(robot_file):
    output = _run_tests_and_process_output(robot_file)
    result = ExecutionResult(output)
    checker = StatusCheckerChecker()
    result.suite.visit(checker)
    checker.print_status()
    sys.exit(len(checker.errors))


def _run_tests_and_process_output(robot_file):
    results = CURDIR / "results"
    output = str(results / "output.xml")
    robot_path = str(CURDIR / robot_file)
    if results.exists():
        shutil.rmtree(results)
    run(robot_path, output=output, log=None, report=None, loglevel="DEBUG")
    process_output(output)
    rebot(output, outputdir=results)
    return output


class StatusCheckerChecker(ResultVisitor):
    def __init__(self):
        self.errors = []
        self.tests = 0

    def visit_test(self, test):
        self.tests += 1
        try:
            self._verify(test)
        except AssertionError as err:
            self.errors.append(str(err))

    def _verify(self, test):
        status, message = self._get_expected(test)
        if test.status != status:
            raise AssertionError(
                f"Test '{test.name}' had wrong status.\n"
                f"{'- ' * 39}\n"
                f"Expected: {status}\n"
                f"Message:\n{message}\n"
                f"{'- ' * 39}\n"
                f"Actual: {test.status}\n"
                f"Message:\n{test.message}"
            )
        if test.message != message:
            raise AssertionError(
                f"Test '{test.name}' had wrong message.\n"
                f"{'- ' * 39}\n"
                f"Expected:\n{message}\n"
                f"{'- ' * 39}\n"
                f"Actual:\n{test.message}"
            )

    def _get_expected(self, test):
        kw = test.setup or test.body[0]
        assert kw.name == "Status", "Status keyword missing!"
        return (kw.body[1].messages[0].message, kw.body[2].messages[0].message)

    def print_status(self):
        print()
        if self.errors:
            print(f"{len(self.errors)}/{self.tests} test failed!")
            print("=" * 78)
            for error in self.errors:
                print(error)
                print("-" * 78)
        else:
            print(f"All {self.tests} tests passed/failed/logged/skipped as expected.")
            print("-" * 78)
        print(
            f"Robot Framework {VERSION} on {python_implementation()} "
            f"{python_version()}."
        )


if __name__ == "__main__":
    check_tests("tests.robot")
