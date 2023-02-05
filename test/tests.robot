*** Settings ***
Suite Setup         Log    Suite setup
Suite Teardown      Log    Suite teardown


*** Test Cases ***
Implicit PASS
    Status    PASS
    No Operation

Explicit PASS with message
    [Documentation]    PASS The message
    Status    PASS    The message
    Pass Execution    The message

Explicit SKIP with message
    [Documentation]    SKIP The message
    [Tags]    rf3unsupported
    Status    SKIP    The message
    Skip    The message

Expected FAIL
    [Documentation]    FAIL Expected failure
    Status    PASS    Test failed as expected.\n\n
    ...    Original message:\nExpected failure
    Fail    Expected failure

SKIP Plus FAIL Expected FAIL
    [Documentation]    SKIP FAIL Expected failure
    [Tags]    rf3unsupported
    Status    PASS    Test failed as expected.\n\n
    ...    Original message:\nExpected failure
    Fail    Expected failure

FAIL Plus SKIP Expected FAIL
    [Documentation]    FAIL Expected failure SKIP
    [Tags]    rf3unsupported
    Status    PASS    Test failed as expected.\n\n
    ...    Original message:\nExpected failure SKIP
    Fail    Expected failure SKIP

Ignore documentation before marker
    [Documentation]    This text is ignored. FAIL Expected failure
    Status    PASS    Test failed as expected.\n\n
    ...    Original message:\nExpected failure
    Fail    Expected failure

Expected FAIL with REGEXP
    [Documentation]    FAIL REGEXP: Pattern is here.* \\d+
    Status    PASS    Test failed as expected.\n\n
    ...    Original message:\nPattern is here\nmultiline 123
    Fail    Pattern is here\nmultiline 123

Expected FAIL with GLOB
    [Documentation]    FAIL GLOB: Globs ??? way *wl\neven *!?!
    Status    PASS    Test failed as expected.\n\n
    ...    Original message:\nGlobs are way kewl\neven in multile lines\n!!!
    Fail    Globs are way kewl\neven in multile lines\n!!!

Expected FAIL with STARTS
    [Documentation]    FAIL STARTS: This is start
    Status    PASS    Test failed as expected.\n\n
    ...    Original message:\nThis is start and this is end
    Fail    This is start and this is end

Log message
    [Documentation]    LOG 2 Hello world!
    Status    PASS
    Log    Hello world!

Log message with message index
    [Documentation]    LOG 2:1 Hello LOG 2:2 world LOG 2:3 !
    Status    PASS
    Log Many    Hello    world    !

Log messages with levels
    [Documentation]    LOG 2 DEBUG Hello
    ...    LOG 3 WARN World
    ...    LOG 4 ERROR Tidii
    Status    PASS
    Log    Hello    DEBUG
    Log    World    WARN
    Log    Tidii    ERROR

Trailing and leading whitespace is ignored in log messages
    [Documentation]
    ...    LOG 2 \${ret} = ${EMPTY}
    ...    LOG 2 \${ret} =
    ...    LOG 3 xxx
    Status    PASS
    ${ret} =    Set Variable    ${EMPTY}
    Log    ${SPACE*10}xxx${SPACE*10}

Log messages deeper
    [Documentation]
    ...    LOG 2:1 Hello
    ...    LOG 2:2 World
    ...    LOG 3.1 DEBUG User Keyword
    ...    LOG 4.1:1 User
    ...    LOG 4.1:2 Keyword
    ...    LOG 5.1:2 DEBUG STARTS: Traceback (most recent call last):
    Status    PASS
    Log Many    Hello    World
    Logging User Keyword
    Logging User Keyword 2
    Run Keyword And Ignore Error
    ...    Fail    My Error Here

Log messages deeper with setup
    [Documentation]
    ...    LOG 1:1 Hello
    ...    LOG 1:2 World
    ...    LOG 2.1 DEBUG User Keyword
    ...    LOG 3.1:1 User
    ...    LOG 3.1:2 Keyword
    ...    LOG 4.1:2 DEBUG STARTS: Traceback (most recent call last):
    [Setup]    Status    PASS
    Log Many    Hello    World
    Logging User Keyword
    Logging User Keyword 2
    Run Keyword And Ignore Error
    ...    Fail    My Error Here

Log messages deeper with wildcard
    [Documentation]
    ...    LOG 2:1 Hello
    ...    LOG 2:2 ANY World
    ...    LOG 3.1 DEBUG User Keyword
    ...    LOG 4.1:* User
    ...    LOG 4.1:* ANY Keyword
    ...    LOG 5.1:* DEBUG STARTS: Traceback (most recent call last):
    ...    LOG 6.1:* ANY REGEXP: .*recent.*
    ...    LOG 6.1:* DEBUG REGEXP: .*recent.*
    Status    PASS
    Log Many    Hello    World
    Logging User Keyword
    Logging User Keyword 2
    Run Keyword And Ignore Error
    ...    Fail    My Error Here
    Run Keyword And Ignore Error
    ...    Fail    'recent call' in two different log levels

Log messages deeper with wildcard and setup
    [Documentation]
    ...    LOG 1:1 Hello
    ...    LOG 1:2 ANY World
    ...    LOG 2.1 DEBUG User Keyword
    ...    LOG 3.1:* User
    ...    LOG 3.1:* ANY Keyword
    ...    LOG 4.1:* DEBUG STARTS: Traceback (most recent call last):
    [Setup]    Status    PASS
    Log Many    Hello    World
    Logging User Keyword
    Logging User Keyword 2
    Run Keyword And Ignore Error
    ...    Fail    My Error Here

Log message with REGEXP
    [Documentation]    LOG 2 REGEXP: H[ei]l{2}o w\\w+! LOG 2 REGEXP: Hell.*
    ...    LOG 3 REGEXP: Multi.*message
    Status    PASS
    Log    Hello world!
    Log    Multi\nline\nmessage

Log message with GLOB
    [Documentation]    LOG 2 GLOB: *world! LOG 2 GLOB: Hell? ***!
    Status    PASS
    Log    Hello world!
    Log    Multi\nline\nmessage

Log message with STARTS
    [Documentation]    LOG 2 STARTS: Hello LOG 2 STARTS: Hell
    ...    LOG 3 STARTS: Multi
    Status    PASS
    Log    Hello world!
    Log    Multi\nline\nmessage

NONE log message
    [Documentation]    LOG 2 NONE LOG 2:1 NONE LOG 3:1 Message LOG 3:2 NONE
    Status    PASS
    No Operation
    Log    Message

Test Setup Check Is Done By SETUP Marker
    [Documentation]    ...
    ...    LOG SETUP:1    NONE
    ...    LOG SETUP.2:1    PASS
    ...    LOG SETUP.2    PASS
    ...    LOG 1:1    KALA
    [Setup]    Status    PASS
    Log    KALA

Error When No Setup
    [Documentation]    ...
    ...    LOG SETUP.1:1    PASS
    ...    LOG 2:1    KALA
    Status    FAIL    Expected test Error When No Setup to have setup but setup is not present.
    Log    KALA

Test Setup Check Is Done By SETUP Marker and wildcard is used
    [Documentation]    ...
    ...    LOG SETUP:1    NONE
    ...    LOG SETUP.2:*    PASS
    ...    LOG SETUP.2    PASS
    ...    LOG 1:*    HAUKI
    [Setup]    Status    PASS
    Log    HAUKI

Error When No Setup and wildcard is used
    [Documentation]    ...
    ...    LOG SETUP.1:*    PASS
    ...    LOG 2:*    KALA
    Status    FAIL    Expected test Error When No Setup and wildcard is used to have setup but setup is not present.
    Log    KALA

Test Teardown Check Is Done By TEARDOWN Marker
    [Documentation]    ...
    ...    LOG TEARDOWN:1    foobar
    ...    LOG TEARDOWN    foobar
    Status    PASS
    [Teardown]    Log    foobar

Error When No Teardown
    [Documentation]    LOG TEARDOWN:1    foobar
    Status    FAIL    Expected test Error When No Teardown to have teardown but teardown is not present.
    Log    KALA

Test Teardown Check Is Done By TEARDOWN Marker and wildcard is used
    [Documentation]    ...
    ...    LOG TEARDOWN:*    foobar
    ...    LOG TEARDOWN    foobar
    Status    PASS
    [Teardown]    Log    foobar

Error When No Teardown and wildcard is used
    [Documentation]    LOG TEARDOWN:*    foobar
    Status    FAIL
    ...    Expected test Error When No Teardown and wildcard is used to have teardown but teardown is not present.
    Log    KALA

Error When NONE is used with wildcard
    [Documentation]    LOG 2.1:* INFO NONE
    Status    FAIL    Message index wildcard '*' is not supported with expected message 'NONE'.
    Logging User Keyword 2

Expected FAIL and log messages
    [Documentation]    This text is ignored. FAIL Told ya!!
    ...    LOG 2 Failing soon!
    ...    LOG 3 Any time now...
    ...    LOG 4:1 FAIL Told ya!!
    ...    LOG 4:2 DEBUG STARTS: Traceback
    Status    PASS    Test failed as expected.\n\n
    ...    Original message:\nTold ya!!
    Log    Failing soon!
    Log    Any time now...
    Fail    Told ya!!

Expected PASS and log messages
    [Documentation]    This text is ignored. PASS Told ya!!
    ...    LOG 2 Passing soon!
    ...    LOG 3 Any time now...
    ...    LOG 4:1 Execution passed with message:\nTold ya!!
    ...    LOG 4:2 NONE
    Status    PASS    Told ya!!
    Log    Passing soon!
    Log    Any time now...
    Pass Execution    Told ya!!

Expected PASS and log messages with COUNT
    [Documentation]
    ...    PASS Told ya!!
    ...    LOG 4 COUNT: 2
    ...    LOG 4:2 NONE
    Status    PASS    Told ya!!
    Log    Passing soon!
    Log    Any time now...
    Pass Execution    Told ya!!

Expected PASS and teadown does not affect
    [Documentation]    This text is ignored.
    ...    LOG 2 Passing soon!
    Status    PASS    ${EMPTY}
    Log    Passing soon!
    [Teardown]    Log    This is logged

FAILURE: Unexpected PASS
    [Documentation]    FAIL Expected failure does not occur
    Status    FAIL    Test was expected to FAIL but it PASSED.
    No Operation

FAILURE: Wrong PASS message
    Status    FAIL    Wrong message.\n\n
    ...    Expected:\n\n\n
    ...    Original message:\nUnexpected message
    Pass Execution    Unexpected message

FAILURE: Unexpected FAIL
    Status    FAIL    Test was expected to PASS but it FAILED.\n\n
    ...    Original message:\n
    ...    Unexpected error message
    Fail    Unexpected error message

FAILURE: Wrong message
    [Documentation]    FAIL Expected failure
    Status    FAIL    Wrong message.\n\n
    ...    Expected:\nExpected failure\n\n
    ...    Original message:\nNot the expected message
    Fail    Not the expected message

FAILURE: Wrong log message
    [Documentation]    LOG 2 Hello world!
    Status    FAIL    Keyword 'BuiltIn.Log' (index 2) message 1 has wrong content.\n\n
    ...    Expected:\nHello world!\n\n
    ...    Actual:\nHi world!
    Log    Hi world!

FAILURE: Wrong log level
    [Documentation]    LOG 2.1 Hello world!
    Status    FAIL    Keyword 'BuiltIn.Log' (index 2.1) message 1 has wrong level.\n\n
    ...    Expected: INFO\n
    ...    Actual: DEBUG
    Logging User Keyword

FAILURE: Unexpected log message
    [Documentation]    LOG 2.1:2 NONE
    Status    FAIL    Keyword 'BuiltIn.Log Many' (index 2.1) message 2 has wrong content.\n\n
    ...    Expected:\nNONE\n\n
    ...    Actual:\nKeyword
    Logging User Keyword 2

FAILURE: Non-existing keyword
    [Documentation]    LOG 2 No keyword here
    Status    FAIL    No keyword with index '2'.

FAILURE: Non-existing log message
    [Documentation]    LOG 2:2 No message here
    Status    FAIL    Keyword 'BuiltIn.Log' (index 2) does not have message 2.
    Log    Message

FAILURE: Non-existing log message wildcard
    [Documentation]    LOG 1:* Bogus message
    Status    FAIL    Keyword 'Status' (index 1) does not contain any logs with level INFO and message 'Bogus message'.


*** Keywords ***
Logging User Keyword
    Log    User Keyword    DEBUG

Logging User Keyword 2
    Log Many    User    Keyword

Status
    [Arguments]    ${status}    @{message}
    ${message} =    Catenate    SEPARATOR=    @{message}
    Log    ${status}
    Log    ${message}
