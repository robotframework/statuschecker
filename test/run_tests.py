#!/usr/env python

import sys

from os import remove
from os.path import abspath, dirname, exists, join
from shutil import rmtree
from subprocess import call

from robot import run, rebot
from robot.api import ExecutionResult, ResultVisitor


CURDIR = dirname(abspath(__file__))
STATUSCHECKER_PATH = join(dirname(CURDIR), 'robotstatuschecker.py')
RESULT_DIR = join(CURDIR, 'results')
OUTPUT = join(RESULT_DIR, 'output.xml')

def check_tests(test_file_path):
    _run_tests_and_statuschecker(test_file_path)
    result = ExecutionResult(OUTPUT)
    checker = StatusCheckerChecker()
    result.visit(checker)
    if checker.errors:
        checker.print_errors()
        sys.exit(len(checker.errors))
    print '\nTests for StatusChecker have completed successfully.'
    sys.exit(0)

def _run_tests_and_statuschecker(test_file_path):
    test_file_path = join(CURDIR, test_file_path)
    if exists(RESULT_DIR):
        rmtree(RESULT_DIR)
    run(test_file_path, log='NONE', report='NONE', outputdir=RESULT_DIR,
        loglevel='DEBUG')
    call(['python', STATUSCHECKER_PATH, OUTPUT])
    rebot(OUTPUT)


class StatusCheckerChecker(ResultVisitor):

    def __init__(self):
        self.errors = []

    def visit_test(self, test):
        kws = test.keywords[0].keywords
        err = (self._check_status(test.status, kws[0].messages[0].message),
               self._check_messages(test.message, kws[1].messages[0].message))
        msg = ''
        if err[0]:
            msg += 'Test "%s" has non-matching status.\n' % test.name
        if err[1]:
            msg += 'Test "%s" has non-matching messages.\n'  % test.name
        if msg:
            self.errors.append(msg)
                
    def _check_status(self, test_status, expected_status):
        return test_status != expected_status

    def _check_messages(self, test_message, expected_message):
        return test_message != expected_message

    def print_errors(self):
        print '\n======\nERRORS\n======\n\n%s' % '------\n'.join(self.errors)


if __name__ == '__main__':
    check_tests('example.txt')
