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

import re
import sys
from os.path import abspath

from robot import __version__ as rf_version
from robot.api import ExecutionResult, ResultVisitor
from robot.utils import Matcher

__version__ = "2.1.0"
RF3 = rf_version.startswith("3")


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
        print(f"Checking {abspath(inpath)}")
    result = StatusChecker().process_output(inpath, outpath)
    if verbose and outpath:
        print(f"Output: {abspath(outpath)}")
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


class Expected:
    def __init__(self, doc):
        self.status = self._get_status(doc)
        self.message = self._get_message(doc)
        self.logs = self._get_logs(doc)

    def _get_status(self, doc):
        return "FAIL" if "FAIL" in doc else "PASS"

    def _get_message(self, doc):
        if "FAIL" not in doc and "PASS" not in doc:
            return ""
        status = self._get_status(doc)
        return doc.split(status, 1)[1].split("LOG", 1)[0].strip()

    def _get_logs(self, doc):
        return [ExpectedLog(item) for item in doc.split("LOG")[1:]]


class ExpectedLog:
    def __init__(self, doc):
        index, message = doc.strip().split(" ", 1)
        test_setup, kw_index, msg_index, test_teardown = self._split_index(index)
        self.test_setup = test_setup
        self.kw_index = kw_index
        self.msg_index = msg_index
        self.test_teardown = test_teardown
        self.level, self.message = self._split_level(message)
        self.visited_setup = False

    @property
    def kw_index_str(self):
        return ".".join(str(index + 1) for index in self.kw_index)

    @property
    def msg_index_str(self):
        return str(self.msg_index + 1) if isinstance(self.msg_index, int) else self.msg_index

    def _split_index(self, index):
        if ":" in index:
            kw_index, msg_index = index.split(":")
        else:
            kw_index, msg_index = index, 1
        new_kw_index = []
        test_setup = False
        test_teardown = False
        for index in kw_index.split("."):
            if index.upper() == "SETUP":
                test_setup = True
                new_kw_index.append(0)
            elif index.upper() == "TEARDOWN":
                test_teardown = True
                new_kw_index.append(-1)
            else:
                new_kw_index.append(int(index) - 1)
        msg_index = "*" if msg_index == "*" else int(msg_index) - 1
        return test_setup, new_kw_index, msg_index, test_teardown

    def _split_level(self, message):
        for level in ["TRACE", "DEBUG", "INFO", "WARN", "FAIL", "ERROR", "ANY"]:
            if message.startswith(level):
                return level, message[len(level) :].strip()
        return "INFO", message


class BaseChecker:
    def _message_matches(self, actual, expected):
        if actual == expected:
            return True
        if expected.startswith("REGEXP:"):
            pattern = f"^{expected.replace('REGEXP:', '', 1).strip()}$"
            if re.match(pattern, actual, re.DOTALL):
                return True
        if expected.startswith("GLOB:"):
            pattern = expected.replace("GLOB:", "", 1).strip()
            matcher = Matcher(pattern, caseless=False, spaceless=False)
            if matcher.match(actual):
                return True
        if expected.startswith("STARTS:"):
            start = expected.replace("STARTS:", "", 1).strip()
            if actual.startswith(start):
                return True
        return False

    def _assert(self, condition, test, message, fail=True):
        if not condition:
            return self._fail(test, message) if fail else False
        return True

    def _fail(self, test, message):
        test.status = "FAIL"
        self._set_message(test, message)
        return False

    def _pass(self, test, message):
        test.status = "PASS"
        self._set_message(test, message)
        return True

    def _set_message(self, test, message):
        if test.message:
            original = f"\n\nOriginal message:\n{test.message}"
        else:
            original = ""
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
        message = f"Test was expected to {self.status} but it {test.status}ED."
        return self._assert(condition, test, message)

    def _check_message(self, test):
        if not self._message_matches(test.message, self.message):
            message = f"Wrong message.\n\nExpected:\n{self.message}"
            return self._fail(test, message)
        if test.status == "FAIL":
            return self._pass(test, "Test failed as expected.")
        return True


class LogMessageChecker(BaseChecker):

    _no_setup_message = "Expected test {} to have setup but setup is not present."
    _no_teardown_message = "Expected test {} to have teardown but teardown is not present."
    _teardown_access_message = (
        "In test '{}' keyword is in teardown but " "was expected to ne in test body index {}"
    )

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
                kw = self._get_keyword_rf3_rf4(test, expected, kw, index)
                if kw is None:
                    return kw
            return kw
        except IndexError:
            message = f"No keyword with index '{expected.kw_index_str}'."
            self._fail(test, message)
            return None

    def _get_keyword_rf3_rf4(self, test, expected, kw, index):
        if RF3:
            return self._get_keyword_rf3(test, expected, kw, index)
        return self._get_keyword_rf4(test, expected, kw, index)

    def _get_keyword_rf3(self, test, expected, kw, index):
        if expected.test_setup and not test.keywords.setup:
            self._fail(test, self._no_setup_message.format(test.name))
            return None
        if expected.test_teardown and not test.keywords.teardown:
            self._fail(test, self._no_teardown_message.format(test.name))
            return None
        if test.keywords.setup and not expected.test_setup and not expected.visited_setup:
            index += 1
            expected.visited_setup = True
        return (kw or test).keywords[index]

    def _get_keyword_rf4(self, test, expected, kw, index):
        if expected.test_setup and not test.setup:
            self._fail(test, self._no_setup_message.format(test.name))
            return None
        if expected.test_teardown and not test.teardown:
            self._fail(test, self._no_teardown_message.format(test.name))
            return None
        if expected.test_setup and not kw:
            kw = test.setup
        elif expected.test_teardown and not kw:
            kw = test.teardown
        else:
            kw = (kw or test).body[index]
        return kw

    def _check_message_by_index(self, test, kw, expected):
        try:
            msg = kw.messages[expected.msg_index]
        except IndexError:
            condition = expected.message == "NONE"
            message = (
                f"Keyword '{kw.name}' (index {expected.kw_index_str}) does not "
                f"have message {expected.msg_index_str}."
            )
            self._assert(condition, test, message)
        else:
            if self._check_msg_level(test, kw, msg, expected):
                self._check_msg_message(test, kw, msg, expected)

    def _check_message_by_wildcard(self, test, kw, expected):
        if expected.message == "NONE":
            message = "Message index wildcard '*' is not supported with expected message 'NONE'."
            self._fail(test, message)
            return

        for msg in kw.messages:
            if self._check_msg_message(test, kw, msg, expected, fail=False):
                if self._check_msg_level(test, kw, msg, expected, fail=False):
                    break
        else:
            message = (
                f"Keyword '{kw.name}' (index {expected.kw_index_str}) does not contain any logs "
                f"with level {expected.level} and message '{expected.message}'."
            )
            self._fail(test, message)

    def _check_message(self, test, kw, expected):
        if expected.msg_index != "*":
            self._check_message_by_index(test, kw, expected)
        else:
            self._check_message_by_wildcard(test, kw, expected)

    def _check_msg_level(self, test, kw, msg, expected, fail=True):
        condition = msg.level == expected.level if expected.level != "ANY" else True
        message = (
            f"Keyword '{kw.name}' (index {expected.kw_index_str}) "
            f"message {expected.msg_index_str} has wrong level."
            f"\n\nExpected: {expected.level}\nActual: {msg.level}"
        )
        return self._assert(condition, test, message, fail)

    def _check_msg_message(self, test, kw, msg, expected, fail=True):
        condition = self._message_matches(msg.message.strip(), expected.message)
        message = (
            f"Keyword '{kw.name}' (index {expected.kw_index_str}) "
            f"message {expected.msg_index_str} has wrong content."
            f"\n\nExpected:\n{expected.message}\n\nActual:\n{msg.message}"
        )
        return self._assert(condition, test, message, fail)


if __name__ == "__main__":
    if "-h" in sys.argv or "--help" in sys.argv:
        print(__doc__)
        sys.exit(251)
    try:
        rc = process_output(*sys.argv[1:])
    except TypeError:
        print(__doc__)
        sys.exit(252)
    sys.exit(rc)
