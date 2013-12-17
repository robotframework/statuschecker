StatusChecker tests
===================

Tests can be run with::

    python run.py

The `<run.py>`_ script runs tests in `<tests.robot>`_ file and verifies
the results with `robotstatuschecker.py <../robotstatuschecker.py>`_.
Tests that have a name starting with *FAILURE:* should end up failing,
other cases should pass.

Test statuses and messages are verified by ``run.py`` based on the
expected status and message logged by ``Status`` keyword. All tests
must use this keyword as their first keyword.
