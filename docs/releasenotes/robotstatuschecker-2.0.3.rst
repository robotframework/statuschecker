========================
robotstatuschecker 2.0.3
========================


.. default-role:: code


StatusChecker is a tool for validating that executed `Robot Framework`_ test cases
have expected statuses and log messages. It is mainly useful for Robot Framework
test library developers who want to use Robot Framework to also test their libraries.
StatusChecker 2.0.1 is compatible with Python 3.6+ and RF 3.2.2 and RF 4.0.1. StatusChecker
2.0.2 fixes regression with 2.0.2 release

StatusChecker project is hosted at GitHub and downloads are at PyPI_

.. _Robot Framework: http://robotframework.org
.. _PyPI: https://github.com/robotframework/statuschecker
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av2.0.3


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

**EXPLAIN** or remove these.

- Revert changes in release 2.0.2, it causes too much other failures (`#29`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#29`_
      - bug
      - critical
      - Revert changes in release 2.0.2, it causes too much other failures

Altogether 1 issue. View on the `issue tracker <https://github.com/robotframework/statuschecker/issues?q=milestone%3Av2.0.3>`__.

.. _#29: https://github.com/robotframework/statuschecker/issues/29
