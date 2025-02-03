StatusChecker tests
===================

Tests can be executed with the `<run.py>`_ script and they should be run
with different Python implementations and versions as needed.

The ``run.py`` script executes tests in ``*.robot`` files and verifies
the results with `robotstatuschecker.py <../robotstatuschecker.py>`_.

Test statuses and messages set by the ``StatusChecker`` are verified by
``run.py``. Every test must use the ``Status`` keyword to specify the expected
status and message.
