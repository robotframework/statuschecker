#!/usr/bin/env python

from os.path import abspath, dirname, exists, join
from platform import python_implementation, python_version
from shutil import rmtree
import sys

from robot import run, rebot
from robot.api import ExecutionResult, ResultVisitor

CURDIR = dirname(abspath(__file__))
sys.path.insert(0, dirname(CURDIR))

from robotstatuschecker import process_output
from robotstatuschecker import RF3


def check_tests(robot_file):
    output = _run_tests_and_process_output(robot_file)
    result = ExecutionResult(output)
    checker = StatusCheckerChecker()
    result.suite.visit(checker)
    checker.print_status()
    sys.exit(len(checker.errors))


def _run_tests_and_process_output(robot_file):
    results = join(CURDIR, "results")
    output = join(results, "output.xml")
    if exists(results):
        rmtree(results)
    run(join(CURDIR, robot_file), output=output, log=None, report=None, loglevel="DEBUG")
    process_output(output)
    rebot(output, outputdir=results)
    return output


class StatusCheckerChecker(ResultVisitor):
    def __init__(self):
        self.errors = []
        self.tests = 0

    def visit_test(self, test):
        self.tests += 1
        status, message = self._get_expected(test)
        errors = [self._verify(test.status, status, "status"), self._verify(test.message, message, "message")]
        errors = ["- %s" % e for e in errors if e]
        if errors:
            self.errors.append("%s:\n%s" % (test.name, "\n".join(errors)))

    def _get_expected(self, test):
        if RF3:
            return self._get_expected_rf3(test)
        return self._get_expected_rf4(test)

    def _get_expected_rf4(self, test):
        if len(test.setup.body) == 0:
            kw = test.body[0]
        else:
            kw = test.setup
        return (kw.body[1].messages[0].message,
                kw.body[2].messages[0].message)

    def _get_expected_rf3(self, test):
        kw = test.keywords[0]
        assert kw.name == "Status", "No 'Status' keyword found."
        return (kw.keywords[1].messages[0].message, kw.keywords[2].messages[0].message)

    def _verify(self, actual, expected, explanation):
        if actual == expected:
            return ""
        return 'Expected %s to be "%s" but it was "%s".' % (explanation, expected, actual)

    def print_status(self):
        print()
        if self.errors:
            print("%d/%d test failed:" % (len(self.errors), self.tests))
            print("\n-------------------------------------\n".join(self.errors))
        else:
            print("All %d tests passed/failed/logged as expected." % self.tests)
        print("Run on %s %s." % (python_implementation(), python_version()))


if __name__ == "__main__":
    check_tests("tests.robot")
