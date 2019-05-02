#!/usr/bin/env python

#  Copyright 2008-2016 Nokia Networks
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

"""Robot Framework test status checker

This tool processes Robot Framework output XML files and checks that test case
statuses and messages are as expected. Main use case is post-processing output
files got when testing Robot Framework test libraries using Robot Framework
itself.

The project is hosted at https://github.com/robotframework/statuschecker/.
See documentation there for the syntax how to specify expected statuses and
log messages.

Command-line usage:

    python -m robotstatuschecker infile [outfile]

Programmatic usage:

    from robotstatuschecker import process_output
    process_output('infile.xml', 'outfile.xml')

If an output file is not given, the input file is edited in place.
"""

from __future__ import print_function

from os.path import abspath
import re
import sys

from robot.api import ExecutionResult, ResultVisitor
from robot.utils import Matcher


__version__ = 'devel'


def process_output(inpath, outpath=None, verbose=True):
    """The main programmatic entry point to status checker.

    Args:
        inpath (str): Path to Robot Framework XML output file to process.
        outpath (str): Path where to write processed output. If not given,
            ``inpath`` is edited in place.
        verbose (bool): When ``True`` (default), prints both ``inpath`` and
            ``outpath`` to console.

    Returns:
        int: Number of failed critical tests after post-processing.
    """
    if verbose:
        print('Checking %s' % abspath(inpath))
    result = StatusChecker().process_output(inpath, outpath)
    if verbose and outpath:
        print('Output: %s' % abspath(outpath))
    return result.return_code


class StatusChecker(ResultVisitor):

    def process_output(self, inpath, outpath=None):
        result = ExecutionResult(inpath)
        result.suite.visit(self)
        result.save(outpath)
        return result

    def visit_test(self, test):
        expected = Expected(test.doc)
        if TestStatusChecker(expected).check(test):
            LogMessageChecker(expected).check(test)

    def visit_keyword(self, kw):
        pass


class Expected(object):

    def __init__(self, doc):
        self.status = self._get_status(doc)
        self.message = self._get_message(doc)
        self.logs = self._get_logs(doc)

    def _get_status(self, doc):
        return 'FAIL' if 'FAIL' in doc else 'PASS'

    def _get_message(self, doc):
        if 'FAIL' not in doc and 'PASS' not in doc:
            return ''
        status = self._get_status(doc)
        return doc.split(status, 1)[1].split('LOG', 1)[0].strip()

    def _get_logs(self, doc):
        return [ExpectedLog(item) for item in doc.split('LOG')[1:]]


class ExpectedLog(object):

    def __init__(self, doc):
        index, message = doc.strip().split(' ', 1)
        self.kw_index, self.msg_index = self._split_index(index)
        self.level, self.message = self._split_level(message)

    @property
    def kw_index_str(self):
        return '.'.join(str(index + 1) for index in self.kw_index)

    @property
    def msg_index_str(self):
        return str(self.msg_index + 1)

    def _split_index(self, index):
        if ':' in index:
            kw_index, msg_index = index.split(':')
        else:
            kw_index, msg_index = index, 1
        kw_index = [int(index) - 1 for index in kw_index.split('.')]
        msg_index = int(msg_index) - 1
        return kw_index, msg_index

    def _split_level(self, message):
        for level in ['TRACE', 'DEBUG', 'INFO', 'WARN', 'FAIL', 'ERROR']:
            if message.startswith(level):
                return level, message[len(level):].strip()
        return 'INFO', message


class BaseChecker(object):

    def _message_matches(self, actual, expected):
        if actual == expected:
            return True
        if expected.startswith('REGEXP:'):
            pattern = '^%s$' % expected.replace('REGEXP:', '', 1).strip()
            if re.match(pattern, actual, re.DOTALL):
                return True
        if expected.startswith('GLOB:'):
            pattern = expected.replace('GLOB:', '', 1).strip()
            matcher = Matcher(pattern, caseless=False, spaceless=False)
            if matcher.match(actual):
                return True
        if expected.startswith('STARTS:'):
            start = expected.replace('STARTS:', '', 1).strip()
            if actual.startswith(start):
                return True
        return False

    def _assert(self, condition, test, message):
        if not condition:
            return self._fail(test, message)
        return True

    def _fail(self, test, message):
        test.status = 'FAIL'
        self._set_message(test, message)
        return False

    def _pass(self, test, message):
        test.status = 'PASS'
        self._set_message(test, message)
        return True

    def _set_message(self, test, message):
        if test.message:
            original = '\n\nOriginal message:\n%s' % test.message
        else:
            original = ''
        test.message = message + original


class TestStatusChecker(BaseChecker):

    def __init__(self, expected):
        self.status = expected.status
        self.message = expected.message

    def check(self, test):
        if self._check_status(test):
            return self._check_message(test)

    def _check_status(self, test):
        condition = test.status == self.status
        message = ('Test was expected to %s but it %sED.'
                   % (self.status, test.status))
        return self._assert(condition, test, message)

    def _check_message(self, test):
        if not self._message_matches(test.message, self.message):
            message = 'Wrong message.\n\nExpected:\n%s' % self.message
            return self._fail(test, message)
        if test.status == 'FAIL':
            return self._pass(test, 'Test failed as expected.')
        return True


class LogMessageChecker(BaseChecker):

    def __init__(self, expected):
        self.logs = expected.logs

    def check(self, test):
        for expected in self.logs:
            kw = self._get_keyword(test, expected)
            if kw:
                self._check_message(test, kw, expected)

    def _get_keyword(self, test, expected):
        kw = None
        try:
            for index in expected.kw_index:
                kw = (kw or test).keywords[index]
            return kw
        except IndexError:
            message = "No keyword with index '%s'." % expected.kw_index_str
            self._fail(test, message)
            return None

    def _check_message(self, test, kw, expected):
        try:
            msg = kw.messages[expected.msg_index]
        except IndexError:
            condition = expected.message == 'NONE'
            message = (
                "Keyword '%s' (index %s) does not have message %s."
                % (kw.name, expected.kw_index_str, expected.msg_index_str))
            self._assert(condition, test, message)
        else:
            if self._check_msg_level(test, kw, msg, expected):
                self._check_msg_message(test, kw, msg, expected)

    def _check_msg_level(self, test, kw, msg, expected):
        condition = msg.level == expected.level
        message = ("Keyword '%s' (index %s) message %s has wrong level.\n\n"
                   "Expected: %s\nActual: %s"
                   % (kw.name, expected.kw_index_str, expected.msg_index_str,
                      expected.level, msg.level))
        return self._assert(condition, test, message)

    def _check_msg_message(self, test, kw, msg, expected):
        condition = self._message_matches(msg.message.strip(), expected.message)
        message = ("Keyword '%s' (index %s) message %s has wrong content.\n\n"
                   "Expected:\n%s\n\nActual:\n%s"
                   % (kw.name, expected.kw_index_str, expected.msg_index_str,
                      expected.message, msg.message))
        return self._assert(condition, test, message)


if __name__ == '__main__':
    if '-h' in sys.argv or '--help' in sys.argv:
        print(__doc__)
        sys.exit(251)
    try:
        rc = process_output(*sys.argv[1:])
    except TypeError:
        print(__doc__)
        sys.exit(252)
    sys.exit(rc)
