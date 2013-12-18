*** Test Cases ***
Expected Pass
    Status    PASS
    No Operation

Expected Pass With Message
    [Documentation]    PASS    The message
    Status    PASS    The message
    Pass Execution    The message

Expected Fail
    [Documentation]  FAIL Expected failure
    Status    PASS    Original test failed as expected.
    Fail  Expected failure

Ignore Text Before Marker
    [Documentation]  This text is ignored. FAIL Expected failure
    Status    PASS    Original test failed as expected.
    Fail  Expected failure

Expected Fail With REGEXP
    [Documentation]  FAIL REGEXP: Pattern is here .* \\d+
    Status    PASS    Original test failed as expected.
    Fail  Pattern is here whatever 123

Expected Fail With STARTS
    [Documentation]  FAIL STARTS: This is start
    Status    PASS    Original test failed as expected.
    Fail  This is start and this is end

Log Message
    [Documentation]  LOG 2 Hello world!
    Status    PASS
    Log  Hello world!

Log Messages With Levels
    [Documentation]  LOG 2 DEBUG Hello LOG 3 WARN World
    Status    PASS
    Log  Hello  DEBUG
    Log  World  WARN

Log Messages Deeper
    [Documentation]  LOG 2:1 Hello LOG 2:2 World
    ...  LOG 3.1 DEBUG User Keyword
    ...  LOG 4.1:1 User LOG 4.1:2 Keyword
    Status    PASS
    Log Many  Hello  World
    Logging User Keyword
    Logging User Keyword 2

Expected Failure And Log Message
    [Documentation]  This text is ignored. FAIL Told ya!!
    ...  LOG 2 Failing soon!
    ...  LOG 3 Any time now...
    ...  LOG 4:1 FAIL Told ya!!
    ...  LOG 4:2 DEBUG STARTS: Traceback
    Status    PASS    Original test failed as expected.
    Log  Failing soon!
    Log  Any time now...
    Fail  Told ya!!

Expected Pass Message And Log Messages
    [Documentation]  This text is ignored. PASS Told ya!!
    ...  LOG 2 Passing soon!
    ...  LOG 3 Any time now...
    ...  LOG 4 Execution passed with message:\nTold ya!!
    Status    PASS    Told ya!!
    Log   Passing soon!
    Log  Any time now...
    Pass Execution    Told ya!!

FAILURE: Unexpected Pass
    [Documentation]  FAIL Expected failure does not occur
    Status    FAIL    Test was expected to FAIL but it PASSED. Expected message:\nExpected failure does not occur
    No Operation

FAILURE: Wrong Pass Message
    Status    FAIL    Wrong error message.\n\nExpected:\n\n\nActual:\nUnexpected message\n
    Pass Execution    Unexpected message

FAILURE: Unexpected Fail
    Status    FAIL    Test was expected to PASS but it FAILED. Error message:\nUnexpected error message
    Fail  Unexpected error message

FAILURE: Wrong Failure Message
    [Documentation]  FAIL Expected failure
    Status    FAIL    Wrong error message.\n\nExpected:\nExpected failure\n\nActual:\nNot the expected message\n
    Fail  Not the expected message

FAILURE: Wrong Log Message
    [Documentation]  LOG 2 Hello world!
    Status    FAIL    Wrong content for message 1 of keyword 'BuiltIn.Log'.\n\nExpected:\nHello world!\n\nActual:\nHi world!
    Log  Hi world!

FAILURE: Wrong Log Level
    [Documentation]  LOG 2 Hello world!
    Status    FAIL    Wrong level for message 1 of keyword 'BuiltIn.Log'.\n\nExpected: INFO\nActual: DEBUG.\nHello world!
    Log  Hello world!  DEBUG


*** Keywords ***
Logging User Keyword
    Log  User Keyword  DEBUG

Logging User Keyword 2
    Log Many  User  Keyword

Status
    [Arguments]    ${status}    ${message}=
    Log    ${status}
    Log    ${message}
