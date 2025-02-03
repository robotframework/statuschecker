*** Test Cases ***
Match message parent
    [Documentation]    LOG 2 Hello world!
    Status    PASS
    Log    Hello world!

Match message directly
    [Documentation]    LOG 2.1 Hello LOG 2.2 world LOG 2.3 !
    Status    PASS
    Log Many    Hello    world    !

Match message using legacy syntax
    [Documentation]    LOG 2:1 Hello LOG 2:2 world LOG 2:3 !
    Status    PASS
    Log Many    Hello    world    !

Messages in child keywords
    [Documentation]
    ...    LOG 2.1 Hello
    ...    LOG 2.2 World
    ...    LOG 3.1 DEBUG User Keyword
    ...    LOG 4.1.1 User
    ...    LOG 4.1.2 Keyword
    ...    LOG 5.1.2 DEBUG STARTS: Traceback (most recent call last):
    Status    PASS
    Log Many    Hello    World
    Logging User Keyword
    Logging User Keyword 2
    Run Keyword And Ignore Error
    ...    Fail    My Error Here

Non-existing keyword
    [Documentation]    LOG 2 No keyword here
    Status    FAIL    Test '${TEST NAME}' does not have child in index 2.

Non-existing child keyword
    [Documentation]    LOG 1.10 No keyword here
    Status    FAIL    Keyword 'Status' (locator '1') does not have child in index 10.

Non-existing message
    [Documentation]    LOG 2.2 No message here
    Status    FAIL    Keyword 'BuiltIn.Log' (locator '2') does not have child in index 2.
    Log    Message

Locator matches keyword
    [Documentation]    LOG 1 Ooops, this locator points to a keyword!
    Status    FAIL    Keyword 'Status' (locator '1') does not have message in index 1.

Locator parent matches message
    [Documentation]    LOG 2.1.666 Ooops, 2.1 is already a message
    Status    FAIL    Locator '2.1' matches message and it cannot have child '666'.
    Log    Hello!

Wrong message
    [Documentation]    LOG 2 Hello world!
    Status    FAIL
    ...    Keyword 'BuiltIn.Log' has wrong message (locator '2').\n\n
    ...    Expected:\nHello world!\n\n
    ...    Actual:\nHi world!
    Log    Hi world!

Log levels
    [Documentation]
    ...    LOG 2    DEBUG  Hello
    ...    LOG 2    ANY    Hello
    ...    LOG 3.1  WARN   World
    ...    LOG 3.1  ANY    World
    ...    LOG 4:1  ERROR  Tidii
    ...    LOG 4:1  ANY    Tidii
    Status    PASS
    Log    Hello    DEBUG
    Log    World    WARN
    Log    Tidii    ERROR

Wrong implicit level
    [Documentation]    LOG 2.1 User Keyword
    Status    FAIL
    ...    Keyword 'BuiltIn.Log' has message with wrong level (locator '2.1').\n\n
    ...    Expected: INFO\n
    ...    Actual: \ \ DEBUG
    Logging User Keyword

Wrong explicit level
    [Documentation]    LOG 2.1 WARN User Keyword
    Status    FAIL
    ...    Keyword 'BuiltIn.Log' has message with wrong level (locator '2.1').\n\n
    ...    Expected: WARN\n
    ...    Actual: \ \ DEBUG
    Logging User Keyword

Messages in test setup and teardown
    [Documentation]
    ...    LOG setup Hello
    ...    LOG SETUP.2 setup
    ...    LOG SeTup.* setup
    ...    LOG TearDown.1 DEBUG User Keyword
    [Setup]    Log Many    Hello    setup
    Status    PASS
    [Teardown]    Logging User Keyword

Test setup missing
    [Documentation]    LOG setup Ooops!
    Status    FAIL    Test '${TEST NAME}' does not have 'setup'.

Test teardown missing
    [Documentation]    LOG TEARDOWN
    Status    FAIL    Test '${TEST NAME}' does not have 'teardown'.

Non-existing attribute
    [Documentation]    LOG nonex Ooops, we did it again!
    Status    FAIL    Test '${TEST NAME}' does not have 'nonex'.

Messages in keyword teardown
    [Documentation]    Keyword setup isn't tested because it isn't supported by all
    ...    Robot versions we support at the moment.
    ...
    ...    LOG 2.teardown.1    DEBUG  User Keyword
    ...    LOG 2.TEARDOWN.1.1  DEBUG  User Keyword
    Status    PASS
    Keyword with teardown

Keyword setup missing
    [Documentation]    LOG    1.setup.666    Ooops...
    Status    FAIL    Keyword 'Status' (locator '1') does not have 'setup'.

Keyword teardown missing
    [Documentation]    LOG    1.teardown.666    Ooops...
    Status    FAIL    Keyword 'Status' (locator '1') does not have 'teardown'.

Match using wildcard
    [Documentation]
    ...    LOG 2.* Hello
    ...    LOG 2.* world
    ...    LOG 3.1.* DEBUG User Keyword
    Status    PASS
    Log Many    Hello    world
    Logging User Keyword

No wildcard match in keyword
    [Documentation]    LOG 1:* Bogus message
    Status    FAIL    Keyword 'Status' (locator '1') has no message matching 'Bogus message' with level INFO.

No wildcard match in test
    [Documentation]    LOG * WARN Bogus message
    Status    FAIL    Test '${TEST NAME}' has no message matching 'Bogus message' with level WARN.

Wildcard parent matches message
    [Documentation]    LOG 2.1.* Ooops, 2.1 is already a message
    Status    FAIL    Locator '2.1' matches message and it cannot have child '*'.
    Log    Hello!

Invalid wildcard usage
    [Documentation]    LOG 1.*.2 Ooops
    Status    FAIL    Message index wildcard '*' can be used only as the last locator item, got '1.*.2'.

NONE
    [Documentation]
    ...    LOG 2   NONE
    ...    LOG 2.1 NONE
    ...    LOG 3.1 Message
    ...    LOG 3.2 NONE
    Status    PASS
    No Operation
    Log    Message

NONE when message exists
    [Documentation]    LOG 2.1.2 NONE
    Status    FAIL
    ...    Keyword 'BuiltIn.Log Many' has wrong message (locator '2.1.2').\n\n
    ...    Expected:\nNONE\n\n
    ...    Actual:\nKeyword
    Logging User Keyword 2

NONE when locator does not match
    [Documentation]    LOG 1.10.2 NONE
    Status    FAIL    Keyword 'Status' (locator '1') does not have child in index 10.

NONE cannot be used with wildcards
    [Documentation]    LOG 1.1:* NONE
    Status    FAIL    Message index wildcard '*' cannot be used with 'NONE' message.

REGEXP
    [Documentation]
    ...    LOG 2 REGEXP: H[ei]l{2}o w\\w+!
    ...    LOG 2 REGEXP: Hell.*
    ...    LOG 3 REGEXP: Multi.*message
    Status    PASS
    Log    Hello world!
    Log    Multi\nline\nmessage

GLOB
    [Documentation]
    ...    LOG 2 GLOB: *world!
    ...    LOG 2 GLOB: Hell? ***!
    Status    PASS
    Log    Hello world!
    Log    Multi\nline\nmessage

STARTS
    [Documentation]
    ...    LOG 2 STARTS: Hello
    ...    LOG 2 STARTS: Hell
    ...    LOG 3 STARTS: Multi
    Status    PASS
    Log    Hello world!
    Log    Multi\nline\nmessage

COUNT
    [Documentation]    This should probably be called LINES instaed.
    ...    LOG 2 COUNT: 3
    Status    PASS
    Log    one\ntwo\nthree

Empty message
    [Documentation]    LOG 2
    Status    PASS
    Log    ${EMPTY}

Leading and trailing whitespace is ignored
    [Documentation]    LOG 2 xxx
    Status    PASS
    Log    ${SPACE*10}xxx${SPACE*10}

Control structure parents
    [Documentation]
    ...    LOG 2.1.1 Hi from IF!
    ...    LOG 3.2.1 Hi from ELSE!
    ...    LOG 4.1.1 a
    ...    LOG 4.2.1 b
    Status    PASS
    IF    True
        Log    Hi from IF!
    END
    IF    False
        Fail    Not run
    ELSE
        Log    Hi from ELSE!
    END
    FOR    ${x}    IN    a    b
        Log    ${x}
    END

Non-existing message with control structure parent
    [Documentation]    LOG 2.1 No message here!
    Status    FAIL    IF (locator '2.1') does not have message in index 1.
    IF    True
        Log    Hi from IF!
    END


*** Keywords ***
Status
    [Arguments]    ${status}    ${message}=Test status has been checked.    @{extra}
    ${message} =    Catenate    SEPARATOR=    ${message}    @{extra}
    Log    ${status}
    Log    ${message}

Logging User Keyword
    Log    User Keyword    DEBUG

Logging User Keyword 2
    Log Many    User    Keyword

Keyword with teardown
    No Operation
    [Teardown]    Logging User Keyword
