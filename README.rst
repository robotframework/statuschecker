StatusChecker
=============

.. contents::
   :local:

Introduction
------------

StatusChecker is a tool for validating that executed `Robot Framework`_
test cases have expected statuses and log messages. It is mainly useful
for Robot Framework test library developers who want to use Robot
Framework to also test their libraries. StatusChecker 1.3 and newer are
compatible both with Python 2 and Python 3.

StatusChecker project is hosted at GitHub_ and downloads are at
PyPI_.

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

Defining expected test status
-----------------------------

By default, all test cases are expected to *PASS* and have no
message. Changing the expected status to *FAIL* is done by having
the word ``FAIL`` (in uppercase) somewhere in the test case
documentation. The expected error message must then follow
the ``FAIL`` marker.

If a test is expected to *PASS* with a certain message, the word
``PASS`` must be added to its documentation explicitly and the
expected message given after that.

If a message check should happen in test setup or teardown, that check
must be prefixed with ``SETUP`` or ``TEARDOWN`` word.

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
    Simple failure
        [Documentation]    FAIL Expected error message
        Steps

    Check in test setup is done by SETUP marker
        [Documentation]    LOG SETUP    This first log message in test setup
        [Setup]    Test specific setup
        Steps

    Exclude documentation before marker
        [Documentation]    This text is ignored FAIL Expected error message
        Steps

    Regexp example
        [Documentation]    FAIL REGEXP: (IOError|OSError): .*
        Steps

    Glob example
        [Documentation]    FAIL GLOB: ??Error: *
        Steps

    Start example
        [Documentation]    FAIL STARTS: IOError:
        Steps

    Passing without message
        Steps

    Passing with message
        [Documentation]    PASS Expected message
        Steps

Defining expected log messages
------------------------------

The expected keyword log messages can also be defined in the test case
documentation using a syntax such as::

   LOG x.y:z LEVEL Actual message

The part before the colon specifies the keyword to check. For
example, ``1`` means first keyword, ``1.2`` is the second child
keyword of the first keyword, and so on.

The part after the colon species the message. For example, ``1:2``
means the second message of the first keyword and ``1.2:3`` is
the third message of the second child keyword of the first keyword.
The message index is optional and defaults to ``1``.
The message index also supports wildcard ``*``. For example ``1:*``
matches any message of the first keyword.

Message level is specified before the actual message, and it can be
any of the valid log levels in capital letters. If the level is not
given it defaults to ``INFO``. Starting from 1.4 release also
``ERROR`` level is supported. The message level also supports wildcard
``ANY`` which will match all log levels.

Possible leading and trailing whitespace is ignored both in the expected
and in the actual log message.

This syntax can be used multiple times to test multiple messages.  It
also works together with specifying the expected error message with
``FAIL``, but it that case ``FAIL`` and the expected error must
be first.

It is also possible to give the message as a regular expression or glob
pattern or to give just the start of the message. This is accomplished
by prefixing the message with ``REGEXP:``, ``GLOB:`` or ``STARTS:``,
respectively, exactly like when `defining expected test status`_.

Finally, to check that a keyword does not have a certain message, it
is possible to use ``NONE`` in the place of the message.

.. sourcecode:: robotframework

    *** Test cases ***
    Simple example
        [Documentation]    LOG 1        Hello, world!
        Steps

    Nested keywords
        [Documentation]    LOG 2.1      1st child of 2nd kw
        Steps

    Message index
        [Documentation]    LOG 2:2      2nd msg of 2nd kw
        Steps

    Nested and index
        [Documentation]    LOG 3.1:2    2nd msg of 3rd kw's 1st child
        Steps

    Log levels
        [Documentation]    LOG 2        DEBUG Debug-level message
        ...                LOG 1.2:3    WARN Warning
        Steps

    Multiple messages
        [Documentation]    LOG 1        First tested message
        ...                LOG 1.2      Second tested message
        ...                LOG 2.2.1    DEBUG Third tested message
        Steps

    Status and log
        [Documentation]    FAIL         Expected error message
        ...                LOG 1.2      Expected log message
        Steps

    Regexp message
        [Documentation]    LOG 1        REGEXP: (Hello|Hi) world!
        Steps

    Glob message
        [Documentation]    LOG 1        GLOB: * world!
        Steps

    Start of the message
        [Documentation]    LOG 1        STARTS: Hello w
        Steps

    No message
        [Documentation]    LOG 1:1      Test that we have only 1 msg
        ...                LOG 1:2      NONE
        Steps
