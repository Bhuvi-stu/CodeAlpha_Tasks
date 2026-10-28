# Security Audit Report — Secure Coding Review

> Historical report from the original Task 3 build. The current review, login rate-limit finding/remediation, 14-test result, and dependency-audit status are documented in [security-review-report.md](security-review-report.md).

**Audit date:** 2026-10-27  
**Scope:** This educational Flask application and its SQLite access code. Testing was limited to this project on localhost.

## 1. Project overview

Secure Coding Review is a local account registration and login application. It stores account records in SQLite, uses Werkzeug password hashing, and provides login, registration, dashboard, and logout flows. The app binds to `127.0.0.1` and starts with Flask debug mode disabled.

## 2. Objectives

The review demonstrates how static analysis and manual review can identify common web application risks, how to remediate them, and how to verify behavior with automated tests and a local HTTP smoke check.

## 3. Technologies used

Python 3.14.6, Flask 3.1.3, Flask-WTF 1.3.0, SQLite, Werkzeug password hashing, Bandit 1.9.4, Pytest 9.1.1, Jinja templates, HTML, and CSS.

## 4. Audit methodology

1. Ran Bandit against the deliberately vulnerable starting source preserved as `reports/initial_app.py` and saved the tool output to `initial_scan.txt`.
2. Manually reviewed the initial and remediated Python code for database handling, password storage, validation, output rendering, CSRF, session configuration, secrets, error handling, and local run settings.
3. Replaced the initial sample with the secured application and ran Bandit against `app.py` and `database.py`.
4. Ran the Pytest security and behavior suite and exercised registration and login through the local HTTP server.

Bandit is a Python static analyzer. It does not establish that all listed vulnerability classes are absent; in particular, it does not fully assess template behavior, runtime configuration, or application logic.

## 5. Initial scan results

The real initial Bandit output is preserved in `reports/initial_scan.txt`. Bandit identified three issues:

| Finding | Severity / confidence | Initial source location | Reason and impact |
|---|---|---|---|
| Flask debug mode enabled (B201) | High / Medium | `reports/initial_app.py:20` | The Werkzeug interactive debugger can permit arbitrary code execution if exposed to an attacker. |
| SQL expression built with string interpolation (B608) | Medium / Low | `reports/initial_app.py:13` | User-controlled `username` was inserted into SQL text, creating a SQL injection path that could alter query behavior or expose records. |
| Hardcoded secret-like value (B105) | Low / Medium | `reports/initial_app.py:6` | A literal development secret was committed in source; anyone with the source could forge signed sessions if the app used this key. |

These line numbers refer to the preserved initial sample, the source scanned for the before report. The initial scan output contains the code context captured by Bandit. Bandit did **not** report every issue in the review scope; input validation, password storage, XSS, CSRF, and cookie behavior required manual review and runtime tests.

## 6. Identified vulnerabilities and severity

The three confirmed initial findings are listed above. Manual review also assessed password handling, input validation, template escaping, CSRF protection, session cookie flags, and error handling. No additional exploitable issue was confirmed in the final code during this limited review. This is not proof that no vulnerabilities remain.

## 7. Evidence and affected source

The initial tool evidence, including Bandit's issue IDs, severities, confidence, line numbers, and source context, is in `reports/initial_scan.txt`. It records a formatted SQL f-string at line 13, a literal Flask secret at line 6, and `app.run(debug=True)` at line 20 of `reports/initial_app.py`.

The final implementation is in `app.py` and `database.py`. The final Bandit output is in `reports/final_scan.txt`. Automated security regression evidence is in `reports/test_results.txt` and `tests/test_security.py`.

## 8. Remediation steps

- Replaced interpolated SQL with SQLite placeholders (`?`) and bound parameters.
- Removed the hardcoded Flask secret. The app reads `SECRET_KEY` from the environment or generates a random per-process secret for local demos; configure a stable secret for a real deployment.
- Disabled debug mode and bound the development server to `127.0.0.1`.
- Used Werkzeug's password hashing and verification functions; plaintext passwords are not persisted.
- Added username and password validation, length limits, and generic login failure messages.
- Used Jinja's autoescaping and Flask-WTF CSRF tokens for forms, including logout.
- Configured session cookies as HttpOnly and SameSite=Lax. The Secure flag can be enabled with `COOKIE_SECURE=true` when using HTTPS; it remains false for local HTTP.
- Added safe user-facing handling for oversized requests and unexpected server errors.

## 9. Fixed code summary

The app now supports registration, authentication, a protected dashboard, and logout. SQLite connections are closed after use and database writes use parameterized SQL. User-facing templates do not render user input as trusted HTML. The app creates its SQLite database under the ignored `instance/` directory by default.

## 10. Actual testing results

`reports/test_results.txt` contains the actual Pytest run:

```text
............                                                             [100%]
12 passed in 2.23s
```

The 12 tests cover registration, valid and invalid login, duplicate users, invalid inputs, password hashing, authenticated dashboard access, logout, CSRF rejection, template escaping, and session cookie settings.

A separate local HTTP smoke check also registered a randomly named test account and successfully reached the dashboard after login. The local server logged HTTP 200 for registration form and dashboard responses and HTTP 302 redirects after registration and login. This smoke check used `instance/live-verification.sqlite3`, which is excluded by `.gitignore`.

## 11. Before-and-after scan comparison

| Scan | Files scanned | Findings |
|---|---|---|
| Initial | Vulnerable snapshot `reports/initial_app.py` | 3 total: 1 High, 1 Medium, 1 Low |
| Final | Remediated `app.py`, `database.py` | 0 reported issues at all severities |

The final scan output reports 111 lines scanned and “No issues identified.” This means Bandit found no matching issues in these two Python files under its configured checks. It does not mean that every possible vulnerability has been excluded.

## 12. Limitations and remaining risks

- The application is for localhost learning and testing, not production identity management.
- There is no login throttling or account lockout, MFA, password reset, email verification, account recovery, or audit trail.
- SQLite and Flask's signed client-side session are used for simplicity. A production deployment needs an explicit session and data protection design.
- The generated fallback secret changes on restart and invalidates sessions. A deployment must supply a securely generated, stable `SECRET_KEY` through its secret manager.
- `COOKIE_SECURE` must be enabled when the application is served over HTTPS. Do not expose the development server directly to the internet.
- No dedicated dependency vulnerability audit, penetration test, production server review, or exhaustive browser testing was performed.
- Bandit does not fully assess HTML templates, configuration, runtime behavior, or every issue category in the requested checklist.

## 13. Conclusion

The initial scan found and documented a hardcoded secret, SQL construction risk, and unsafe Flask debug setting. The remediated app uses environment-based secret configuration, parameterized SQL, and debug-disabled localhost serving. The final Bandit scan reported zero issues, all 12 automated tests passed, and a local HTTP registration/login smoke check succeeded. The project is suitable as a local educational example, with the deployment limitations above remaining relevant.
