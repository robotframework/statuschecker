Usage
=====

.. sourcecode :: bash

    $ python run_tests.py

This test script first runs *example.txt*, only generating *output.xml*. Then
it runs *robotstatuschecker.py* to mark test cases either passed or failed
depending on the documentation of the test case. Finally, it will use *rebot* to 
create a log and a report file based on the changed *output.xml*. The script 
will then traverse the result, checking that cases that should have passed 
and failed are respectively marked correctly based on the first keyword 
*Status* in the test cases. It also checks that log messages are correct based
on this keyword.

Test cases with the name beginning *FAILURE:* should end up failing, other cases
should pass.