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

Status with log message
    [Documentation]    This text is ignored.
    ...    FAIL Expected
    ...    LOG 1.2 PASS
    ...    LOG 2   Hello!
    ...    LOG 3.1 FAIL Expected
    ...    LOG 3.2 DEBUG STARTS: Traceback
    Status    PASS
    ...    ${CHECKED}\n\n
    ...    Original status: FAIL\n\n
    ...    Original message:\nExpected
    Log     Hello!
    Fail    Expected

*** Keywords ***
Status
    [Arguments]    ${status}    ${message}=${CHECKED}    @{extra}
    ${message} =    Catenate    SEPARATOR=    ${message}    @{extra}
    Log    ${status}
    Log    ${message}
