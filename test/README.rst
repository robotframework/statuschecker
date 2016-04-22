StatusChecker tests
===================

Tests can be executed with the `<run.py>`_ script and they should be run
with different Python implementations and versions as needed::

    python run.py
    jython run.py
    ipy run.py
    python3 run.py

The ``run.py`` script executes tests in `<tests.robot>`_ file and verifies
the results with `robotstatuschecker.py <../robotstatuschecker.py>`_.
Tests that have a name starting with *FAILURE:* should end up failing,
other tests should pass.

Test statuses and messages set by StatusChecker are verified by ``run.py``.
Expected statuses and messages are logged by ``Status`` keyword that all
tests must use as their first keyword.
