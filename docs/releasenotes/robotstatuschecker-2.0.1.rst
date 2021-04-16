========================
robotstatuschecker 2.0.1
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
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av2.0.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

statuschecker works different with different RF versions (`#26`_)
-----------------------------------------------------------------
Release 2.0.0 added support for SETUP and TEARDOWN markers, but also
introduced regression when test had test setup and log messages
where checked.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#26`_
      - bug
      - critical
      - statuschecker works different with different RF versions

Altogether 1 issue. View on the `issue tracker <https://github.com/robotframework/statuschecker/issues?q=milestone%3Av2.0.1>`__.

.. _#26: https://github.com/robotframework/statuschecker/issues/26
