#!/usr/bin/env python

# Copyright 2008-2015 Nokia Networks
# Copyright 2016-     Robot Framework Foundation
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

"""Robot Framework status checker.

This tool processes Robot Framework output XML files and checks that test case
statuses and messages are as expected. Main use case is post-processing output
files got when testing Robot Framework test libraries using Robot Framework
itself.

The project is hosted at https://github.com/robotframework/statuschecker/.
See documentation there for the syntax how to specify expected statuses and
log messages.

Command-line usage:

    python -m robotstatuschecker infile [outfile]  [true]

Programmatic usage:

    from robotstatuschecker import process_output
    process_output('infile.xml', 'outfile.xml')

If an output file is not given, the input file is edited in place.
"""

import re
import sys
from os.path import abspath, normpath
from pathlib import Path

from robot.api import ExecutionResult, ResultVisitor
from robot.model import BodyItem  # type: ignore
from robot.result import Keyword, Message, Result, TestCase  # type: ignore
from robot.utils import Matcher  # type: ignore

__version__ = "4.1.0"


def process_output(in_path: "str|Path", out_path: "str|Path|None" = None) -> int:
    """The main programmatic entry point to status checker.

    Args:
        in_path: Path to Robot Framework XML output file to process.
        out_path: Path where to write processed output. If not given,
            `in_path` is edited in place.

    Returns:
        Number of failed tests after post-processing.
    """
    # Use os.path functions because pathlib has no way to normalize paths
    # without also resolving symlinks.
    in_path = abspath(normpath(in_path))
    out_path = abspath(normpath(out_path)) if out_path else None
    print(f"Checking {in_path}")
    result = StatusChecker().check(in_path, out_path)
    if out_path:
        print(f"Output: {out_path}")
    return result.return_code


class StatusChecker(ResultVisitor):
    def check(self, in_path: "str|Path", out_path: "str|None" = None) -> Result:
        result = ExecutionResult(str(in_path))  # Old RF versions do not accept Path.
        result.suite.visit(self)
        result.save(out_path)
        return result

    def visit_test(self, test: TestCase):
        expected = Expected(test.doc)
        if StatusAndMessageChecker(expected).check(test):
            if LogMessageChecker(expected).check(test):
                self._mark_checked(test)

    def _mark_checked(self, test: TestCase):
        message = "Test status has been checked."
        if test.status != "PASS":
            message += f"\n\nOriginal status: {test.status}"
        if test.message:
            message += f"\n\nOriginal message:\n{test.message}"
        test.status = "PASS"
        test.message = message

    def visit_keyword(self, kw: Keyword):
        pass


class Expected:
    def __init__(self, doc: str):
        status, logs = self._split_status_and_logs(doc)
        self.status = self._get_status(status)
        self.message = self._get_message(status)
        self.logs = self._get_logs(logs)

    def _split_status_and_logs(self, doc: str) -> "tuple[str, str]":
        if "LOG" not in doc:
            return doc, ""
        log_index = doc.find("LOG")
        status_indices = [
            doc.find(status) for status in ("FAIL", "SKIP", "PASS") if status in doc
        ]
        if not status_indices or log_index < min(status_indices):
            return "", doc
        return doc[:log_index], doc[log_index:]

    def _get_status(self, config: str) -> str:
        if "FAIL" in config:
            return "FAIL"
        if "SKIP" in config:
            return "SKIP"
        return "PASS"

    def _get_message(self, config: str) -> str:
        for status in ["FAIL", "SKIP", "PASS"]:
            if status in config:
                return config.split(status, 1)[1].strip()
        return ""

    def _get_logs(self, config: str) -> "list[ExpectedLog]":
        return [ExpectedLog(item) for item in config.split("LOG")[1:]]


class ExpectedLog:
    def __init__(self, doc: str):
        try:
            locator, message = doc.strip().split(maxsplit=1)
        except ValueError:
            locator, message = doc.strip(), ""
        self.locator_str = locator
        # ':' is legacy message separator. It was softly deprecated in v4.0.
        self.locator = [
            self._parse_locator_part(part)
            for part in locator.replace(":", ".").split(".")
        ]
        self.level, self.message = self._split_level(message)

    def _parse_locator_part(self, part: str) -> "int|str":
        try:
            return int(part)
        except ValueError:
            return part.lower()

    def _split_level(self, message: str) -> "tuple[str, str]":
        for level in ["TRACE", "DEBUG", "INFO", "WARN", "FAIL", "ERROR", "ANY"]:
            if message.startswith(level):
                return level, message[len(level) :].strip()
        return "INFO", message


class BaseChecker:
    def _message_matches(self, actual: str, expected: str) -> bool:
        if actual == expected:
            return True
        if expected.startswith("REGEXP:"):
            pattern = expected.replace("REGEXP:", "", 1).strip()
            if re.fullmatch(pattern, actual, re.DOTALL):
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

    def _fail(self, test: TestCase, message: str):
        test.status = "FAIL"
        if test.message:
            test.message = f"{message}\n\nOriginal message:\n{test.message}"
        else:
            test.message = message


class StatusAndMessageChecker(BaseChecker):
    def __init__(self, expected: Expected):
        self.status = expected.status
        self.message = expected.message

    def check(self, test: TestCase) -> bool:
        if test.status != self.status:
            self._fail(test, f"Expected {self.status} status, got {test.status}.")
            return False
        if not self._message_matches(test.message, self.message):
            self._fail(test, f"Wrong message.\n\nExpected:\n{self.message}")
            return False
        return True


class LogMessageChecker(BaseChecker):
    def __init__(self, expected: Expected):
        self.logs = expected.logs

    def check(self, test: TestCase):
        for expected in self.logs:
            try:
                self._check(test, expected)
            except CheckOk:
                pass
            except (InvalidUsage, NotFound, AssertionError) as err:
                self._fail(test, str(err))
                return False
        return True

    def _check(self, test: TestCase, expected: ExpectedLog):
        item = test
        for level, part in enumerate(expected.locator):
            if isinstance(item, Message):
                locator = ".".join(str(part) for part in expected.locator[:level])
                raise NotFound(
                    f"Locator '{locator}' matches message and it cannot have "
                    f"child '{part}'."
                )
            if part == "*":
                self._check_message_by_wildcard(item, expected, level)
                return
            if isinstance(part, int):
                item = self._get_item_by_index(item, part, expected, level)
            else:
                item = self._get_item_by_attribute(item, part, expected, level)
        if not isinstance(item, Message):
            item = self._get_item_by_index(item, 1, expected, require_message=True)
        assert isinstance(item, Message)
        self._check_message(item, expected)

    def _get_item_by_index(
        self,
        parent: "TestCase|BodyItem",
        index: int,
        expected: ExpectedLog,
        level: "int|None" = None,
        require_message: bool = False,
    ) -> "BodyItem":
        prefix = self._get_error_prefix(parent, expected.locator[:level])
        try:
            item = self._flatten(parent.body)[index - 1]
            if item.type == item.MESSAGE or not require_message:
                return item
            raise NotFound(f"{prefix} does not have message in index {index}.")
        except IndexError:
            if expected.message == "NONE" and (
                level is None or len(expected.locator) == level + 1
            ):
                raise CheckOk
            raise NotFound(f"{prefix} does not have child in index {index}.")

    def _flatten(self, body) -> "list[BodyItem]":
        try:
            return body.flatten()
        except AttributeError:  # Body.flatten() is new in RF 5.0.
            flattened = []
            for item in body:
                if item.type in ("IF/ELSE ROOT", "TRY/EXCEPT ROOT"):
                    flattened.extend(item.body)
                else:
                    flattened.append(item)
            return flattened

    def _get_item_by_attribute(
        self,
        parent: "TestCase|BodyItem",
        attribute: str,
        expected: ExpectedLog,
        level: int,
    ) -> "BodyItem":
        item = getattr(parent, attribute, None)
        if item:
            return item
        prefix = self._get_error_prefix(parent, expected.locator[:level])
        raise NotFound(f"{prefix} does not have '{attribute}'.")

    def _get_error_prefix(
        self, parent: "TestCase|BodyItem", locator: "list[str|int]"
    ) -> str:
        if isinstance(parent, TestCase):
            prefix = f"Test '{self._get_name(parent)}'"
        elif isinstance(parent, Keyword):
            prefix = f"Keyword '{self._get_name(parent)}'"
        else:
            prefix = parent.type
        if locator:
            prefix += f" (locator '{'.'.join(str(part) for part in locator)}')"
        return prefix

    def _get_name(self, item: "TestCase|BodyItem") -> str:
        if isinstance(item, TestCase):
            return item.name
        if isinstance(item, Keyword):
            # `full_name` is new in RF 7.0. With older `name` returns the full name.
            return getattr(item, "full_name", item.name)
        return item.type

    def _check_message_by_wildcard(
        self, parent: "TestCase|Message", expected: ExpectedLog, level: int
    ):
        if len(expected.locator) != level + 1:
            raise InvalidUsage(
                f"Message index wildcard '*' can be used only as "
                f"the last locator item, got '{expected.locator_str}'."
            )
        if expected.message == "NONE":
            raise InvalidUsage(
                "Message index wildcard '*' cannot be used with 'NONE' message."
            )
        for item in parent.body:
            if (
                isinstance(item, Message)
                and self._message_matches(item.message.strip(), expected.message)
                and self._level_matches(item.level, expected.level)
            ):
                return
        prefix = self._get_error_prefix(parent, expected.locator[:level])
        raise AssertionError(
            f"{prefix} has no message matching '{expected.message}' with "
            f"level {expected.level}."
        )

    def _level_matches(self, actual: str, expected: str) -> bool:
        return expected in (actual, "ANY")

    def _check_message(self, message: Message, expected: ExpectedLog):
        name = self._get_name(message.parent)
        locator = expected.locator_str
        if not self._message_matches(message.message.strip(), expected.message):
            raise AssertionError(
                f"Keyword '{name}' has wrong message "
                f"(locator '{locator}').\n\n"
                f"Expected:\n{expected.message}\n\n"
                f"Actual:\n{message.message}"
            )
        if not self._level_matches(message.level, expected.level):
            raise AssertionError(
                f"Keyword '{name}' has message with wrong level "
                f"(locator '{locator}').\n\n"
                f"Expected: {expected.level}\n"
                f"Actual:   {message.level}"
            )


class InvalidUsage(Exception):
    pass


class NotFound(Exception):
    pass


class CheckOk(Exception):
    pass


if __name__ == "__main__":
    args = sys.argv[1:]
    if "-h" in args or "--help" in args or len(args) not in (1, 2):
        print(__doc__)
        sys.exit(251)
    rc = process_output(*args)
    sys.exit(rc)
