========================
robotstatuschecker 2.0.0
========================


.. default-role:: code


StatusChecker is a tool for validating that executed `Robot Framework`_ test cases
have expected statuses and log messages. It is mainly useful for Robot Framework
test library developers who want to use Robot Framework to also test their libraries.
StatusChecker 2 and newer are compatible both with Python 3.6+ and Robot Framework 3.2
4.0.

StatusChecker project is hosted at GitHub and downloads are at PyPI_
.. _Robot Framework: http://robotframework.org
.. _PyPI: https://github.com/robotframework/statuschecker
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av2.0.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Broken with RF4 (`#11`_)
------------------------
Status checker is not compatible with RF 4.0 and does not anymore display
warning when it uses RF result parser.

Add SETUP and TEARDOWN markers for checking logs from test setup and teardown (`#21`_)
--------------------------------------------------------------------------------------
In previous releases keywords in setup and teardown could have been referenced
index starting from 1. If setup was present, then index one would point the
setup keyword. But if setup was not present, index 1 would point to the first
keyword in test body. This is somewhat confusing and now keywords is setup and
teardown must be targeted by using SETUP and TEARDOWN markers. Also index one
will always point to the first keyword in the test body.

Backwards incompatible changes
==============================

Drop Python 2 support and use Python 3.6 is minimum version.  (`#14`_)
----------------------------------------------------------------------
This release drops support for Python 2 and raises minimum version Python to
3.6. Also Robot Framework 3.2 and 4.0 are supported by this release.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#11`_
      - bug
      - critical
      - Broken with RF4
    * - `#14`_
      - enhancement
      - critical
      - Drop Python 2 support and use Python 3.6 is minimum version. 
    * - `#21`_
      - enhancement
      - high
      - Add SETUP and TEARDOWN markers for checking logs from test setup and teardown

Altogether 3 issues. View on the `issue tracker <https://github.com/robotframework/statuschecker/issues?q=milestone%3Av2.0.0>`__.

.. _#11: https://github.com/robotframework/statuschecker/issues/11
.. _#14: https://github.com/robotframework/statuschecker/issues/14
.. _#21: https://github.com/robotframework/statuschecker/issues/21
