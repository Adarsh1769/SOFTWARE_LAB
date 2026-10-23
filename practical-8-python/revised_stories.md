# Revised user stories

## [REQ-01] Create an account

As a visitor, I want to register with a unique email and a compliant password
so that I can create a secure account.

Acceptance criteria:
- Given: an email address not already registered. When: I submit a password with at least 12 characters, one uppercase letter, and one digit. Then: my account is created and the password is stored using a non-plain-text representation.
- Given: an email address already registered or a password missing any required rule. When: I submit registration. Then: the system rejects the request and explains the validation error.

## [REQ-02] Verify an email address

As a new user, I want to verify my email using a time-limited link so that I can securely activate my account.

Acceptance criteria:
- Given: a newly registered account. When: the system sends its verification link and I open it within 24 hours. Then: my email is marked verified.
- Given: an expired verification link or an unverified account. When: I use the link or attempt to sign in. Then: the link is rejected or sign-in is denied, respectively.

## [REQ-03] Sign in

As a registered user, I want to sign in with my verified email and password so that I can access my account.

Acceptance criteria:
- Given: a verified account that is not locked. When: I submit the correct password. Then: I am signed in and the consecutive failed-attempt counter is reset.
- Given: an incorrect password. When: five consecutive sign-in attempts fail. Then: the account is locked for 15 minutes and further attempts during that period are denied.
- Given: an unverified account. When: I submit the correct password. Then: sign-in is denied until I verify my email.

## [REQ-04] Reset a forgotten password

As a user who forgot my password, I want to reset it using a one-time link so that I can regain access securely.

Acceptance criteria:
- Given: that I request a reset. When: the system sends a reset link and I use it within 30 minutes. Then: I can set a new password and sign in with it.
- Given: an expired or previously used reset link. When: I try to use it. Then: the system rejects the request and does not change my password.
