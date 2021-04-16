========================
robotstatuschecker 2.0.2
========================


.. default-role:: code


StatusChecker is a tool for validating that executed `Robot Framework`_ test cases
have expected statuses and log messages. It is mainly useful for Robot Framework
test library developers who want to use Robot Framework to also test their libraries.
StatusChecker 2.0.1 is compatible with Python 3.6+ and RF 3.2.2 and RF 4.0.1. StatusChecker
2.0.1 fixes regression with Rf 3.2.2 when test has test setup.

StatusChecker project is hosted at GitHub and downloads are at PyPI_
.. _Robot Framework: http://robotframework.org
.. _PyPI: https://github.com/robotframework/statuschecker
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av2.0.2


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Keywords teardown in RF 3 could be accessed without TEARDOWN marker (`#28`_)
----------------------------------------------------------------------------
Keywords teardown in RF 3 could be accessed without TEARDOWN marker. It as
used as is, but it should raise an error.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#28`_
      - bug
      - critical
      - Keywords teardown in RF 3 could be accessed without TEARDOWN marker

Altogether 1 issue. View on the `issue tracker <https://github.com/robotframework/statuschecker/issues?q=milestone%3Av2.0.2>`__.

.. _#28: https://github.com/robotframework/statuschecker/issues/28
