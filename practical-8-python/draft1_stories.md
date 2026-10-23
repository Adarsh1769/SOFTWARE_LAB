# Draft 1 - AI-generated user stories

## [REQ-01] Create an account

As a visitor, I want to register with my email and password.

Acceptance criteria:
- Given: a new email and a valid password. When: I submit registration. Then: my account is created.
- Given: an email already in use. When: I submit registration. Then: registration is rejected.

## [REQ-02] Verify an email address

As a new user, I want to verify my email so that I can access my account.

Acceptance criteria:
- Given: a new account. When: its owner opens the verification link. Then: the account is verified.
- Given: an unverified account. When: the user tries to sign in. The sign-in is denied.

## [REQ-03] Sign in

As a registered user, I want to sign in so that I can use my account.

Acceptance criteria:
- Given: an account. When: the user enters a wrong password five times. Then: the account is locked.
