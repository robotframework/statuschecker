*** Test Cases ***
Expected Pass
    Status    PASS
    No Operation

Expected Fail
    [Documentation]  Texts before fail (in caps) is ignored. FAIL Expected failure
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
    [Documentation]  FAIL Failing now! LOG 2 Failing soon!
    Status    PASS    Original test failed as expected.
    Log  Failing soon!
    Fail  Failing now!

FAILURE: Unexpected Pass
    [Documentation]  FAIL Expected failure does not occur
    Status    FAIL    Test was expected to FAIL but it PASSED. Expected message:\nExpected failure does not occur
    No Operation

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
