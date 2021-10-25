========================
robotstatuschecker 2.1.0
========================


.. default-role:: code


StatusChecker is a tool for validating that executed `Robot Framework`_ test cases
have expected statuses and log messages. It is mainly useful for Robot Framework
test library developers who want to use Robot Framework to also test their libraries.
StatusChecker 1.4 and newer are compatible with Python 3.6+.

StatusChecker project is hosted at GitHub and downloads are at PyPI_
.. _Robot Framework: http://robotframework.org
.. _PyPI: https://github.com/robotframework/statuschecker
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av2.1.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Wildcard support for the log verification (`#32`_)
--------------------------------------------------
Now it possible to verify keyword log messages with a wildcard (*), example with 1:*.
This allows to verify that log massage is somewhere in the keyword, but specific index
of the log message is not mandatory anymore.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#32`_
      - enhancement
      - high
      - Wildcard support for the log verification

Altogether 1 issue. View on the `issue tracker <https://github.com/robotframework/statuschecker/issues?q=milestone%3Av2.1.0>`__.

.. _#32: https://github.com/robotframework/statuschecker/issues/32
