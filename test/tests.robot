*** Settings ***
Suite Setup         Log    Suite setup
Suite Teardown      Log    Suite teardown


*** Variables ***
${CHECKED} =    Test status has been checked.


*** Test Cases ***
Expected implicit PASS
    Status    PASS
    No Operation

Expected explicit PASS
    [Documentation]    PASS The message
    Status    PASS
    ...    ${CHECKED}\n\n
    ...    Original message:\nThe message
    Pass Execution    The message

Expect PASS got FAIL
    Status    FAIL
    ...    Expected PASS status, got FAIL.\n\n
    ...    Original message:\nOoops!
    Fail    Ooops!

Expect PASS got SKIP
    Status    FAIL
    ...    Expected PASS status, got SKIP.\n\n
    ...    Original message:\nOoops!
    Skip    Ooops!

PASS with wrong message
    [Documentation]    PASS The message
    Status    FAIL
    ...    Wrong message.\n\n
    ...    Expected:\nThe message

Expected SKIP
    [Documentation]    SKIP The message
    Status    PASS
    ...    ${CHECKED}\n\n
    ...    Original status: SKIP\n\n
    ...    Original message:\nThe message
    Skip    The message

Expect SKIP got PASS
    [Documentation]    SKIP This won't happen!
    Status    FAIL    Expected SKIP status, got PASS.

Expect SKIP got FAIL
    [Documentation]    SKIP This won't happen!
    Status    FAIL
    ...    Expected SKIP status, got FAIL.\n\n
    ...    Original message:\nThis happens!
    Fail    This happens!

SKIP with wrong message
    [Documentation]    SKIP The message
    Status    FAIL
    ...    Wrong message.\n\n
    ...    Expected:\nThe message\n\n
    ...    Original message:\nxxx
    Skip    xxx

Expected FAIL
    [Documentation]    Text before the marker is ignored. FAIL Expected failure
    Status    PASS
    ...    ${CHECKED}\n\n
    ...    Original status: FAIL\n\n
    ...    Original message:\nExpected failure
    Fail    Expected failure

Expect FAIL got PASS
    [Documentation]    FAIL This won't happen!
    Status    FAIL    Expected FAIL status, got PASS.

Expect FAIL got SKIP
    [Documentation]    FAIL This won't happen!
    Status    FAIL
    ...    Expected FAIL status, got SKIP.\n\n
    ...    Original message:\nThis happens!
    Skip    This happens!

FAIL with wrong message
    [Documentation]    FAIL Wrong
    Status    FAIL
    ...    Wrong message.\n\n
    ...    Expected:\nWrong\n\n
    ...    Original message:\nMessage
    Fail    Message

FAIL with REGEXP
    [Documentation]    FAIL REGEXP: Pattern is here.* \\d+
    Status    PASS
    ...    ${CHECKED}\n\n
    ...    Original status: FAIL\n\n
    ...    Original message:\nPattern is here\nmultiline 123
    Fail    Pattern is here\nmultiline 123

FAIL with GLOB
    [Documentation]    FAIL GLOB: Globs ??? way *wl\neven *!?!
    Status    PASS
    ...    ${CHECKED}\n\n
    ...    Original status: FAIL\n\n
    ...    Original message:\nGlobs are way kewl\neven in multile lines\n!!!
    Fail    Globs are way kewl\neven in multile lines\n!!!

FAIL with STARTS
    [Documentation]    FAIL STARTS: This is start
    Status    PASS
    ...    ${CHECKED}\n\n
    ...    Original status: FAIL\n\n
    ...    Original message:\nThis is start and this is end
    Fail    This is start and this is end

Log matching message parent
    [Documentation]    LOG 2 Hello world!
    Status    PASS
    Log    Hello world!

Log matching message
    [Documentation]    LOG 2.1 Hello world!
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

Invalid wildcard usage
    [Documentation]    LOG 1.*.2 Ooops
    Status    FAIL    Message index wildcard '*' can be used only as the last locator item, got '1.*.2.

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

Empty log message
    [Documentation]    LOG 2
    Status    PASS
    Log    ${EMPTY}

NONE log message
    [Documentation]
    ...    LOG 2    NONE
    ...    LOG 2:1 NONE
    ...    LOG 3:1 Message
    ...    LOG 3:2 NONE
    Status    PASS
    No Operation
    Log    Message

NONE log message when locator does not match
    [Documentation]    LOG 1.10.2 NONE
    Status    FAIL    Keyword 'Status' (locator '1') does not have child in index 10.

Test Setup Check Is Done By SETUP Marker
    [Documentation]
    ...    LOG SETUP:10    NONE
    ...    LOG SETUP.2:1    PASS
    ...    LOG SETUP.2    PASS
    ...    LOG 1:1    KALA
    [Setup]    Status    PASS
    Log    KALA

Error When No Setup
    [Documentation]
    ...    LOG setup.1:1    PASS
    ...    LOG 2:1    KALA
    Status    FAIL    Test '${TEST NAME}' does not have 'setup'.
    Log    KALA

Test Setup Check Is Done By SETUP Marker and wildcard is used
    [Documentation]
    ...    LOG SETUP:10    NONE
    ...    LOG SETUP.2:*    PASS
    ...    LOG SETUP.2    PASS
    ...    LOG 1:*    HAUKI
    [Setup]    Status    PASS
    Log    HAUKI

Test Teardown Check Is Done By TEARDOWN Marker
    [Documentation]
    ...    LOG TEARDOWN:1    foobar
    ...    LOG TEARDOWN    foobar
    Status    PASS
    [Teardown]    Log    foobar

Error When No Teardown
    [Documentation]    LOG TEARDOWN:1    foobar
    Status    FAIL    Test '${TEST NAME}' does not have 'teardown'.
    Log    KALA

Test Teardown Check Is Done By TEARDOWN Marker and wildcard is used
    [Documentation]
    ...    LOG TEARDOWN:*    foobar
    ...    LOG TEARDOWN    foobar
    Status    PASS
    [Teardown]    Log    foobar

Keyword teardown
    [Documentation]    Keyword setup isn't tested because it isn't supported by all
    ...    Robot versions we support at the moment.
    ...
    ...    LOG    2.teardown.1    DEBUG    User Keyword
    ...    LOG    2.TEARDOWN.1:1 DEBUG    User Keyword
    Status    PASS
    Keyword with teardown

No keyword teardown
    [Documentation]    LOG    1.teardown.666    Ooops...
    Status    FAIL    Keyword 'Status' (locator '1') does not have 'teardown'.

Error When NONE is used with wildcard
    [Documentation]    LOG 2.1:* INFO NONE
    Status    FAIL    Message index wildcard '*' cannot be used with 'NONE' message.
    Logging User Keyword 2

Expected FAIL and log messages
    [Documentation]    This text is ignored. FAIL Told ya!!
    ...    LOG 2 Failing soon!
    ...    LOG 3 Any time now...
    ...    LOG 4:1 FAIL Told ya!!
    ...    LOG 4:2 DEBUG STARTS: Traceback
    Status    PASS
    ...    ${CHECKED}\n\n
    ...    Original status: FAIL\n\n
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
    Status    PASS
    ...    ${CHECKED}\n\n
    ...    Original message:\nTold ya!!
    Log    Passing soon!
    Log    Any time now...
    Pass Execution    Told ya!!

Expected PASS and log messages with COUNT
    [Documentation]
    ...    PASS Told ya!!
    ...    LOG 4 COUNT: 2
    ...    LOG 4:2 NONE
    Status    PASS
    ...    ${CHECKED}\n\n
    ...    Original message:\nTold ya!!
    Log    Passing soon!
    Log    Any time now...
    Pass Execution    Told ya!!

FAILURE: Wrong log message
    [Documentation]    LOG 2 Hello world!
    Status    FAIL
    ...    Keyword 'BuiltIn.Log' has wrong message (locator '2').\n\n
    ...    Expected:\nHello world!\n\n
    ...    Actual:\nHi world!
    Log    Hi world!

FAILURE: Wrong implicit log level
    [Documentation]    LOG 2.1 User Keyword
    Status    FAIL
    ...    Keyword 'BuiltIn.Log' has message with wrong level (locator '2.1').\n\n
    ...    Expected: INFO\n
    ...    Actual: \ \ DEBUG
    Logging User Keyword

FAILURE: Wrong explicit log level
    [Documentation]    LOG 2.1 WARN User Keyword
    Status    FAIL
    ...    Keyword 'BuiltIn.Log' has message with wrong level (locator '2.1').\n\n
    ...    Expected: WARN\n
    ...    Actual: \ \ DEBUG
    Logging User Keyword

FAILURE: Unexpected log message
    [Documentation]    LOG 2.1:2 NONE
    Status    FAIL
    ...    Keyword 'BuiltIn.Log Many' has wrong message (locator '2.1:2').\n\n
    ...    Expected:\nNONE\n\n
    ...    Actual:\nKeyword
    Logging User Keyword 2

FAILURE: Non-existing keyword
    [Documentation]    LOG 2 No keyword here
    Status    FAIL    Test 'FAILURE: Non-existing keyword' does not have child in index 2.

FAILURE: Non-existing child keyword
    [Documentation]    LOG 1.10 No keyword here
    Status    FAIL    Keyword 'Status' (locator '1') does not have child in index 10.

FAILURE: Non-existing log message
    [Documentation]    LOG 2:2 No message here
    Status    FAIL    Keyword 'BuiltIn.Log' (locator '2') does not have child in index 2.
    Log    Message

FAILURE: Non-existing log message wildcard
    [Documentation]    LOG 1:* Bogus message
    Status    FAIL    Keyword 'Status' (locator '1') has no message matching 'Bogus message' with level INFO.

FAILURE: Non-existing message in test with wildcard
    [Documentation]    LOG * WARN Bogus message
    Status    FAIL    Test '${TEST NAME}' has no message matching 'Bogus message' with level WARN.

FAILURE: Log locator matches keyword
    [Documentation]    LOG 1 Ooops, this locator points to a keyword.
    Status    FAIL    Keyword 'Status' (locator '1') does not have message in index 1.

FAILURE: Log locator parent matches message
    [Documentation]    LOG 2.1.666 Ooops, 2.1 is already a message
    Status    FAIL    Locator '2.1' matches message and it cannot have child '666'.
    Log    Hello!

FAILURE: Log locator parent with wildcard matches message
    [Documentation]    LOG 2.1.* Ooops, 2.1 is already a message
    Status    FAIL    Locator '2.1' matches message and it cannot have child '*'.
    Log    Hello!

# Control structures
#    Fail    FIXME
#
# Invalid attribute
#    Fail    FIXME


*** Keywords ***
Logging User Keyword
    Log    User Keyword    DEBUG

Logging User Keyword 2
    Log Many    User    Keyword

Keyword with teardown
    No Operation
    [Teardown]    Logging User Keyword

Status
    [Arguments]    ${status}    ${message}=${CHECKED}    @{extra}
    ${message} =    Catenate    SEPARATOR=    ${message}    @{extra}
    Log    ${status}
    Log    ${message}
