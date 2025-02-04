StatusChecker
=============

.. contents::
   :local:

Introduction
------------

StatusChecker is a tool for validating that executed `Robot Framework`_
tests have expected statuses and log messages. It is mainly useful
for Robot Framework library developers who want to test their libraries
using Robot Framework.

StatusChecker project is hosted at GitHub_ and downloads are at PyPI_.

.. _Robot Framework: http://robotframework.org
.. _GitHub: https://github.com/robotframework/statuschecker
.. _PyPI: https://pypi.python.org/pypi/robotstatuschecker
.. _pip: http://pip-installer.org

Installation instructions
-------------------------

The easiest way to install StatusChecker is by using pip_::

    pip install robotstatuschecker

Alternatively you can get the code by cloning the project from
GitHub_ or downloading the source distribution from PyPI_ and
extracting it. After that you can install the tool with::

    python setup.py install

Usage
-----

From the command line::

    python -m robotstatuschecker infile [outfile]

Programmatically:

.. sourcecode:: python

    from robotstatuschecker import process_output

    process_output('infile.xml', 'outfile.xml')

If an output file is not given, the input file is edited in place.
If you want to get a log and a report, you need to use the Rebot tool
separately afterwards.

Defining expected test status
-----------------------------

By default, all tests are expected to *PASS* and have no message.
Changing the expected status to *FAIL* is done by having the word
``FAIL`` (case-sensitive) somewhere in the test documentation.
The expected error message must then follow the ``FAIL`` marker.

If the test is expected to be skipped, you can change the expected status
to *SKIP* by adding the word ``SKIP`` in the documentation. Also in
this case the expected message must follow the marker. If a test is
expected to *PASS* with a certain message, the word ``PASS`` must be
added to its documentation explicitly and the expected message given
after that.

The expected message can also be specified as a regular expression by
prefixing it with ``REGEXP:``. The specified regular expression
must match the error message fully. Having spaces between the status,
the message and the possible regular expression prefix is optional.

An alternative to using regular expressions is using glob patterns where
``*`` matches anything (including newline) and ``?`` matches any single
character. This is can be accomplished by starting the expected message
with ``GLOB:``.

Finally, it is possible to test that the message starts with something
by prefixing the expected message with ``STARTS:``.

The following examples illustrate different ways to define test
statuses and messages:

.. sourcecode:: robotframework

    *** Test Cases ***
    Implicit PASS
        Log    Hello!

    Explicit PASS with message
        [Documentation]    PASS Expected message
        Pass Execution    Expected message

    Expected FAIL
        [Documentation]    FAIL Expected failure
        Fail    Expected failure

    Expected SKIP
        [Documentation]    Text before marker is ignored SKIP Expected skip
        Skip    Expected skip

    Message using REGEXP
        [Documentation]    FAIL REGEXP: (IOError|OSError): .*
        Fail    IOError: Unknown error

    Message using GLOB
        [Documentation]    FAIL GLOB: ??Error: *
        Fail    IOError: Unknown error

    Message using STARTS
        [Documentation]    FAIL STARTS: IOError:
        Fail    IOError: Unknown error


Defining expected log messages
------------------------------

In addition to verifying test statuses and messages, it possible to verify
messages logged by keywords. Expected log messages are defined in the test
documentation using this syntax::

   LOG x.y.z LEVEL Actual message

The syntax consists of the following parts:

- ``LOG`` marker (case-sensitive).
- Locator used for finding the message. Locators typically consists of 1-based
  indices like ``2.1.3`` matching items in test and keyword body. In addition
  to that, they can contain ``setup`` and ``teardown`` markers mathing test and
  keyword setup and teardown.
- Optional, case-sensitive log level. If omitted, the level is ``INFO``.
  Special value ``ANY`` can be used to accept any level.
- The actual log message. Possible leading and trailing whitespace is ignored.
  Special value ``NONE`` (case-sensitive) can be used to indicate that there
  should be no log message.

The locator can either point directly to the message to be verified or
to the parent element of the message. In the latter case the actual message
is expected to be the first item in parent's body. If the message index
is not known, it is possible use the asterisk as a wildcard like ``2.*``
to match any message. When a locator points directly to a message, it is
possible to use ``:`` as the message separator instead of ``.``, but this
support is deprecated and may be removed in the future.

If test status and message is also tested, they must be specified before
the ``LOG`` marker using the syntax explained in the previous section.
If there are multiple message to be tested, the ``LOG`` marker can be used
multiple times. In such cases it is often a good idea to split the documentation
to multiple lines.

.. sourcecode:: robotframework

    *** Test cases ***
    Locator points to message parent
        [Documentation]    LOG 1 Hello! LOG 2 first LOG 3.1 Nested!
        Log    Hello!
        Log Many    first    second    third
        User Keyword

    Locator points to directly to message
        [Documentation]    Splitting can enhance readability. This text is ignored.
        ...    LOG 1.1 Hello!
        ...    LOG 2.2 second
        ...    LOG 3.1.1 Nested!
        Log    Hello!
        Log Many    first    second    third
        User Keyword

    Message in setup and teardown
        [Documentation]
        ...    LOG    setup         Hello!
        ...    LOG    teardown.1    Nested!
        [Setup]    Log    Hello!
        No Operation
        [Teardown]    User Keyword

    Wildcard
        [Documentation]    LOG 1.* first
        Log Many    first    second    third

    No message
        [Documentation]
        ...    LOG    1.1    one
        ...    LOG    1.2    two
        ...    LOG    1.3    NONE
        Log Many    one    two

    Log levels
        [Documentation]
        ...    LOG    1    DEBUG    first
        ...    LOG    2    INFO     second
        ...    LOG    3    ANY      third
        Log    first    level=DEBUG
        Log    second   level=INFO
        Log    third    level=DEBUG

    Test status and log message
        [Documentation]    FAIL    Expected failure
        ...    LOG    1    INFO    Hello!
        ...    LOG    2    FAIL    Expected failure
        Log    Hello!
        Fail    Expected failure

    *** Keywords ***
    User Keyword
        Log    Nested!

If the message is not known exactly, it is possible to match it as a regular
expression or glob pattern or to give just the beginning of the message.
This is accomplished by prefixing the message with ``REGEXP:``, ``GLOB:``
or ``STARTS:``, respectively, exactly like when `defining expected test status`_.

.. sourcecode:: robotframework

    *** Test cases ***
    Log message using REGEXP
        [Documentation]    LOG 1 REGEXP: Hello, .*!
        Log    Hello, Robots!

    Log message using GLOB
        [Documentation]    LOG 1 GLOB: Hello, *!
        Log    Hello, Robots!

    Log message using STARTS
        [Documentation]    LOG 1 STARTS: Hello
        Log    Hello, Robots!
