#!/usr/bin/env python

import sys

from os import remove
from os.path import abspath, dirname, exists, join
from shutil import rmtree
from subprocess import call

from robot import run, rebot
from robot.api import ExecutionResult, ResultVisitor


CURDIR = dirname(abspath(__file__))
STATUSCHECKER = join(dirname(CURDIR), 'robotstatuschecker.py')
RESULTS = join(CURDIR, 'results')


def check_tests(test_file_path):
    output = _run_tests_and_statuschecker(test_file_path)
    result = ExecutionResult(output)
    checker = StatusCheckerChecker()
    result.visit(checker)
    checker.print_status()
    sys.exit(len(checker.errors))

def _run_tests_and_statuschecker(test_file):
    test_file = join(CURDIR, test_file)
    output = join(RESULTS, 'output.xml')
    if exists(RESULTS):
        rmtree(RESULTS)
    run(test_file, log='NONE', report='NONE', outputdir=RESULTS,
        loglevel='DEBUG')
    call(['python', STATUSCHECKER, output])
    rebot(output, outputdir=RESULTS)
    return output


class StatusCheckerChecker(ResultVisitor):

    def __init__(self):
        self.errors = []
        self.tests = 0

    def visit_test(self, test):
        self.tests += 1
        status, message = self._get_expected(test)
        errors = [self._verify(test.status, status, 'status'),
                  self._verify(test.message, message, 'message')]
        errors = ['- %s' % e for e in errors if e]
        if errors:
            self.errors.append('%s:\n%s' % (test.name, '\n'.join(errors)))

    def _get_expected(self, test):
        kw = test.keywords[0]
        assert kw.name == 'Status', "No 'Status' keyword found."
        return (kw.keywords[0].messages[0].message,
                kw.keywords[1].messages[0].message)

    def _verify(self, actual, expected, explanation):
        if actual == expected:
            return ''
        return ('Expected %s to be "%s" but it was "%s".'
                % (explanation, expected, actual))

    def print_status(self):
        print
        if self.errors:
            print '%d/%d test failed:' % (len(self.errors), self.tests)
            print '\n-------------------------------------\n'.join(self.errors)
        else:
            print 'All %d tests passed/failed/logged as expected.' % self.tests


if __name__ == '__main__':
    check_tests('tests.robot')
