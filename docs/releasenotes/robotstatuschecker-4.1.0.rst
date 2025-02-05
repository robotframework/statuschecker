========================
robotstatuschecker 4.1.0
========================


.. default-role:: code


StatusChecker is a tool for validating that executed `Robot Framework`_ test cases
have expected statuses and log messages. It is mainly useful for Robot Framework
library developers who want to use Robot Framework to also test their libraries.

StatusChecker project is hosted at GitHub and downloads are at PyPI_
.. _Robot Framework: http://robotframework.org
.. _PyPI: https://github.com/robotframework/statuschecker
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av4.1.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Inline flags don't work in REGEXP mode (`#45`_)
------------------------------------------------
Regex match did not allow to use inline flags like `(?i)` or `(?s)`. This is now allowed.

Backwards incompatible changes
==============================

Remove broken functionality to count messages using (`#53`_)
------------------------------------------------------------
COUNT is now removed from the library. It was broken and not used by anyone.

Acknowledgements
================

Cannot use the FAIL log level if test itself does not FAIL (`#4`_)
------------------------------------------------------------------
Many thanks for Joao Coelho for providing initial PR to for problem when there's no log
level PASS and if test is expected to pass but to have FAIL messages.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#45`_
      - bug
      - high
      - Inline flags don't work in REGEXP mode
    * - `#53`_
      - enhancement
      - high
      - Remove broken functionality to count messages using
    * - `#4`_
      - bug
      - medium
      - Cannot use the FAIL log level if test itself does not FAIL
    * - `#9`_
      - enhancement
      - medium
      - Document that StatusChecker can be used as pre-Rebot modifier

Altogether 4 issues. View on the `issue tracker <https://github.com/robotframework/statuschecker/issues?q=milestone%3Av4.1.0>`__.

.. _#45: https://github.com/robotframework/statuschecker/issues/45
.. _#53: https://github.com/robotframework/statuschecker/issues/53
.. _#4: https://github.com/robotframework/statuschecker/issues/4
.. _#9: https://github.com/robotframework/statuschecker/issues/9
