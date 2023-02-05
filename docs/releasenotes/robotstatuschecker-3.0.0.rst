========================
robotstatuschecker 3.0.0
========================


.. default-role:: code


StatusChecker is a tool for validating that executed `Robot Framework`_ test cases
have expected statuses and log messages. It is mainly useful for Robot Framework
test library developers who want to use Robot Framework to also test their libraries.
StatusChecker 3 Python 3.

StatusChecker project is hosted at GitHub and downloads are at PyPI_
.. _Robot Framework: http://robotframework.org
.. _PyPI: https://github.com/robotframework/statuschecker
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av3.0.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Add support for counting messages (`#39`_)
------------------------------------------
Sometimes it is handy just count the keyword messages. Now it is possible
to use COUNT 


Backwards incompatible changes
==============================

Support RF 5 and 6 (`#40`_)
---------------------------
Now only RF 5 and 6 are supported.


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#39`_
      - enhancement
      - high
      - Add support for counting messages
    * - `#40`_
      - enhancement
      - high
      - Support RF 5 and 6

Altogether 2 issues. View on the `issue tracker <https://github.com/robotframework/statuschecker/issues?q=milestone%3Av3.0.0>`__.

.. _#39: https://github.com/robotframework/statuschecker/issues/39
.. _#40: https://github.com/robotframework/statuschecker/issues/40
