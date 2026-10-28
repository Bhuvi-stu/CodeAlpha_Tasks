# Secure Coding Review - Security Review Report

**Reviewed:** 2026-10-27  
**Application:** Existing beginner-level Flask registration/login application  
**Scope:** `app.py`, `database.py`, templates, tests, requirements and project documentation. Testing was limited to this local project.

## Executive summary

The existing account creation, sign-in, sign-out, and protected dashboard features were retained. Review confirmed safe password hashing, parameterized SQLite statements, CSRF protection, template autoescaping, input validation, and session clearing on sign-out. One current finding was confirmed: the original login route did not limit repeated password attempts. It is now limited to five POST attempts per minute per client IP. The new regression test verifies the limit.

The final Bandit scan reports no issues in the application Python files. The updated suite passes 14 tests, including the original 12 behaviors and new rate-limit and ASCII username checks. A dependency audit was attempted but did not complete because the PyPI TLS certificate could not be verified; dependency security remains unverified by pip-audit.

## Application and method

The app is written in Python with Flask and SQLite. Review combined manual inspection of Python, HTML templates, session/configuration behavior, and regression tests with Bandit static analysis. pip-audit was added for dependency auditing; its attempted run and exact limitation are recorded in `dependency_audit.txt`.

Bandit is a static analyzer, not a complete web security test. A zero-issue result is limited to the scanned Python source and Bandit's rules. HTML behavior, runtime deployment settings, and third-party package advisories require separate checks.

## Confirmed finding from the reviewed project

| Finding | Severity | Affected code | Impact | Remediation and retest |
|---|---|---|---|---|
| Login endpoint had no rate limit | Medium | Original `app.py`, login POST handler (current route at `app.py:63-65`) | An attacker could make repeated password guesses against an account, increasing the chance of credential guessing. | Added Flask-Limiter at five POST attempts per minute per client IP (`app.py:64`). `test_login_rate_limit_blocks_excessive_attempts` confirms five invalid attempts receive the normal invalid-login response and the next attempt receives HTTP 429. |

## Historical findings in the intentionally vulnerable starting sample

These are findings in the preserved starting sample `reports/initial_app.py`, not in the current application. The real initial scan is `reports/initial_scan.txt`.

| Finding | Initial severity / confidence | Initial location | Impact | Fix in current code |
|---|---|---|---|---|
| Flask debug mode enabled (B201) | High / Medium | `reports/initial_app.py:20` | If exposed, the Werkzeug debugger can enable arbitrary code execution. | Current app binds to `127.0.0.1` and runs with `debug=False` (`app.py:115`). |
| SQL assembled with user input (B608) | Medium / Low | `reports/initial_app.py:13` | Crafted input could alter a database query and expose or change data. | Queries bind the username as a SQL parameter (`database.py:17-22`). |
| Hardcoded secret-like value (B105) | Low / Medium | `reports/initial_app.py:6` | A source-visible signing key could allow forged Flask session cookies. | Current app reads `SECRET_KEY` from the environment and generates only a random per-process local fallback (`app.py:24`). |

## Manual review of the current application

- **Password handling:** `generate_password_hash` and `check_password_hash` are used (`app.py:11,55,70`). Tests verify stored data is a hash and the original password verifies.
- **SQL injection:** Usernames are passed through `?` placeholders in SQLite statements (`database.py:17-22,26-30`). No interpolated user input is used in SQL.
- **Input validation:** Registration enforces 3-30 ASCII alphanumeric/underscore usernames and 12-128 character passwords (`app.py:103-112`). Invalid-input cases are tested.
- **XSS:** Templates use ordinary Jinja interpolation, which autoescapes HTML. The regression test verifies a script-like username is rendered as text.
- **CSRF:** Flask-WTF CSRF protection is initialized globally; registration, login, and sign-out forms include tokens. Missing-token POST is tested.
- **Session and sign-out:** Cookies are HttpOnly and SameSite=Lax; Secure is configurable for HTTPS. Login clears the prior session before setting identity. Sign-out is POST-only, CSRF-protected, and clears session state. A test confirms the dashboard redirects after sign-out.
- **Secrets:** No production key is hardcoded. The local fallback changes on restart; deployments must set a stable secret through a secret manager.
- **Errors:** Unexpected server errors return a generic response while details go to server logs; oversized requests receive HTTP 413.
- **Rate limiting:** Login POST attempts are limited to five per minute per IP. The default `memory://` counter is only process-local; Flask-Limiter cautions against using it as production storage, so multi-worker deployments need shared storage such as Redis and trusted proxy configuration ([Flask-Limiter configuration](https://flask-limiter.readthedocs.io/en/stable/configuration.html)).
- **Dependencies:** `pip-audit` is configured as a project tool, but its actual advisory lookup failed due a TLS certificate error. No claim is made that dependencies passed an audit. See `dependency_audit.txt`.

## Recommendations

1. Before deployment, supply a stable `SECRET_KEY` from a secret manager and enable secure cookies over HTTPS.
2. For multiple workers, configure Flask-Limiter to use shared Redis storage; do not rely on process-local memory counters.
3. Re-run pip-audit after fixing the local TLS/network trust issue and review any advisories before release.
4. Keep dependencies updated, avoid committing `.env` or SQLite files, and run tests and Bandit in CI.
5. Treat this as a localhost learning project. It does not include MFA, password recovery, account lockout, HTTPS termination, production session storage, or a full deployment hardening review.

## Retest results

Commands run from the project root:

```powershell
python -m pytest tests -q
python -m bandit -f txt -o reports\final_scan.txt app.py database.py
```

Actual Pytest result: `14 passed in 2.22s` (see `reports/test_results.txt`). The original 12 tests remain and two checks were added: the login rate limit and ASCII-only username validation.

Actual final Bandit result: `No issues identified`; 122 lines scanned across `app.py` and `database.py`, zero issues at all severities (see `reports/final_scan.txt`). The intentionally vulnerable initial scan remains separate in `reports/initial_scan.txt`.

Dependency audit status: **not completed** due certificate verification failure when connecting to PyPI. `reports/dependency_audit.txt` records the error and command to retry.

## Conclusion

The existing application features remain intact. The confirmed login brute-force control gap was remediated and tested. The final Bandit scan and full test suite passed. Dependency vulnerability status remains unknown until pip-audit can reach its advisory source with a valid certificate chain.
