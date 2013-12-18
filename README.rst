StatusChecker
=============

StatusChecker is a tool for checking that `Robot Framework`_ test
cases have expected statuses and log messages. It is mainly useful for
Robot Framework test library developers who want to use Robot
Framework to also test their libraries.

StatusChecker project is hosted in BitBucket_ and downloads are in
PyPI_.

.. _Robot Framework: http://robotframework.org
.. _BitBucket: https://bitbucket.org/robotframework/statuschecker
.. _PyPI: https://pypi.python.org/pypi/robotstatuschecker

Installation instructions
=========================

The easiest way to install StatusChecker is by using `pip`_:

.. sourcecode:: bash

    $ pip install robotstatuschecker

Alternatively you can get the code by cloning the project from
BitBucket_ or downloading the source distribution from PyPI_ and
extracting it. After that you can install the tool with:

.. sourcecode:: bash

    $ python setup.py install

.. _pip: http://pip-installer.org


Usage
=====

From the command line:

.. sourcecode:: bash

    $ python -m robotstatuschecker infile [outfile]

Programmatically:

.. sourcecode:: python

    from robotstatuschecker import process_output
    process_output('infile.xml', 'outfile.xml')

If an output file is not given, the input file is considered to be
also an output file and it is edited in place.

Defining expected test status
=============================

By default, all test cases are expected to *PASS* and have no
message. Changing the expected status to *FAIL* is done by having
the word ``FAIL`` (in uppercase) somewhere in the test case
documentation. The expected error message must then be given after
the ``FAIL`` text.

If a test is expected to *PASS* with a certain message, the word
``PASS`` must be added to its documentation explicitly and the
expected message given after that. This is a new feature in version
1.1.

The expected message can also be specified as a regular expression by
prefixing it with ``REGEXP:``. The specified regular expression
must match the error message fully. Having spaces between the status,
the message and the possible regular expression prefix is optional.

It is also possible to test only the beginning of the error by
prefixing the expected message with ``STARTS:``.

The following examples illustrate different ways to define test
statuses and messages:

.. sourcecode :: robotframework

    *** Test cases ***
    Simple Example
        [Documentation]    FAIL Expected error message
        Steps

    Exclude Documentation Before Marker
        [Documentation]    This text is ignored FAIL Expected error message
        Steps

    Regexp Example
        [Documentation]    FAIL REGEXP: (IOError|OSError): .*
        Steps

    Start Example
        [Documentation]    FAIL STARTS: IOError:
        Steps

    Passing Without Message
        Steps

    Passing With Message
        [Documentation]    PASS Expected message
        Steps

Defining expected log messages
==============================

The expected keyword log messages can also be defined in the test case
documentation using a syntax such as::

   LOG x.y:z LEVEL Actual message

The part before the colon is the number of the keyword to check. For
example ``1`` means first keyword, ``1.2`` is the second child
keyword of the first keyword, and so on.

The part after the colon denotes the number of the message. For
example ``1:2`` means the second message of the first keyword and
``1.2:3`` is the third message of the second child keyword of the
first keyword. The message index is optional and defaults to ``1``.

Message level is specified before the actual message, and it can be
any of the valid log levels in capital letters. If the level is not
given it defaults to ``INFO``.

This syntax can be used multiple times to test multiple messages.  It
also works together with specifying the expected error message with
``FAIL``, but it that case ``FAIL`` and the expected error must
be first.

The log message can also be given as a regular expression pattern the
same way as the `expected error message`__. Finally, to check that a
keyword does not have a certain message, it is possible to use
``NONE`` in the place of the message.

__ `Defining expected test status`_

.. sourcecode :: robotframework

    *** Test cases ***
    Simple Example
        [Documentation]    LOG 1        Hello, world!
        Steps

    Nested Keywords
        [Documentation]    LOG 2.1      1st child of 2nd kw
        Steps

    Message Index
        [Documentation]    LOG 2:2      2nd msg of 2nd kw
        Steps

    Nested and Index
        [Documentation]    LOG 3.1:2    2nd msg of 3rd kw's 1st child
        Steps

    Log levels
        [Documentation]    LOG 2        DEBUG Debug-level message
        ...                LOG 1.2:3    WARN Warning 
        Steps

    Multiple Messages
        [Documentation]    LOG 1        First tested message
        ...                LOG 1.2      Second tested message
        ...                LOG 2.2.1    DEBUG Third tested message
        Steps

    Status and Log
        [Documentation]    FAIL         Expected error message
        ...                LOG 1.2      Expected log message
        Steps

    Regexp Message
        [Documentation]    LOG 1        REGEXP: (Hello|Hi) world!
        Steps

    No Message
        [Documentation]    LOG 1:1      Test that we have only 1 msg
        ...                LOG 1:2      NONE
        Steps
