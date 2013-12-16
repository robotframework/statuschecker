#!/usr/bin/env python

#  Copyright 2008-2013 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import sys

from os import remove
from os.path import abspath, dirname, exists, join
from subprocess import call

from robot import run, rebot
from robot.api import ExecutionResult, ResultVisitor

def check_tests(test_file_path):
    output_path = _run_tests_and_statuschecker(test_file_path)
    result, checker = ExecutionResult(output_path), StatusCheckerChecker()
    result.visit(checker)
    if checker.errors:
        checker.print_errors()
        sys.exit(len(checker.errors))
    print '\nTests for StatusChecker have completed successfully.'
    sys.exit(0)

def _run_tests_and_statuschecker(test_file_path):
    (test_file_path, curdir,
     status_checker_path, output_path) = _get_paths(test_file_path)
    _remove_old_files(curdir)
    run(test_file_path, log='NONE', report='NONE', outputdir=curdir,
        loglevel='DEBUG')
    call(['python', status_checker_path, output_path])
    rebot(output_path, outputdir=curdir)
    return output_path

def _get_paths(test_file_path):
    curdir = dirname(abspath(__file__))
    return (join(curdir, test_file_path),
            curdir,
            join(dirname(curdir), 'robotstatuschecker.py'),
            join(curdir, 'output.xml'))

def _remove_old_files(target_dir):
    for path in ['report.html', 'log.html', 'output.xml']:
        path = join(target_dir, path)
        if exists(path):
            remove(path)

class StatusCheckerChecker(ResultVisitor):

    def __init__(self):
        self.errors = []

    def visit_test(self, test):
        kws = test.keywords[0].keywords
        self.check(test.name, test.status, kws[0].messages[0].message,
                   test.message, kws[1].messages[0].message)

    def check(self, test_name, test_status, expected_status, test_message,
              expected_message):
        msg = self._check_status(test_name, test_status, expected_status)
        msg = self._check_messages(msg, test_name, test_message,
                                   expected_message)
        if msg:
            self.errors.append(msg)

    def _check_status(self, test_name, test_status, expected_status):
        msg = ''
        if expected_status == 'FAIL':
            if test_status != expected_status:
                msg = 'Test "%s" should have failed but passed.' % test_name
        else:
            if test_status != expected_status:
                msg = 'Test "%s" should have passed but failed.' % test_name
        return msg

    def _check_messages(self, msg, test_name, test_message, expected_message):
        if test_message != expected_message:
            if not msg:
                prefix = 'Test "%s" ' % test_name
            else:
                prefix = '\n\nAlso, test '
            msg += prefix + 'does not have correct messages:\n\n"%s"\n!=\n"%s"'\
                            % (test_message, expected_message)
        return msg if msg else ''

    def print_errors(self):
        print '\n%s' % '\n------\n'.join(self.errors)


if __name__ == '__main__':
    check_tests('example.txt')
