========================
robotstatuschecker 3.0.1
========================


.. default-role:: code


StatusChecker is a tool for validating that executed `Robot Framework`_ test cases
have expected statuses and log messages. It is mainly useful for Robot Framework
test library developers who want to use Robot Framework to also test their libraries.
StatusChecker 1.4 and newer are compatible both with Python 2 and Python 3.

StatusChecker project is hosted at GitHub and downloads are at PyPI_
.. _Robot Framework: http://robotframework.org
.. _PyPI: https://github.com/robotframework/statuschecker
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av3.0.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

RF 6.1 support (`#44`_)
-----------------------
When test looks like this:

Test
    [Documentation]    LOG 1:1    KALA
    Log    KALA

prior RF 6.1 doc was returned like: LOG 1:1 KALA, with single pace
between 1.1 and KALA. But in RF 6.1 doc is returned as is. This
causes problem in validation message and being backwards compatible.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#44`_
      - bug
      - critical
      - RF 6.1 support

Altogether 1 issue. View on the `issue tracker <https://github.com/robotframework/statuschecker/issues?q=milestone%3Av3.0.1>`__.

.. _#44: https://github.com/robotframework/statuschecker/issues/44
