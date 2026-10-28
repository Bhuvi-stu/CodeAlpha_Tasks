# Secure Coding Review

A beginner friendly, local only Flask registration and login application built to demonstrate a source code security review. It uses SQLite, Werkzeug password hashing, Flask-WTF CSRF protection, Flask-Limiter, parameterized SQL, validated input, secure cookie defaults, and autoescaped Jinja templates.

## Features and objectives

- Register, sign in, view an authenticated dashboard, and sign out.
- Store password hashes instead of plaintext passwords.
- Reject invalid usernames and weak or oversized passwords.
- Use parameterized database queries, CSRF tokens, and generic login errors.
- Limit sign-in attempts to five POST requests per minute per client IP.
- Keep the app bound to `127.0.0.1` with Flask debug mode disabled.
- Compare an initial Bandit scan with the scan after remediation and run regression tests.

## Technologies

Python 3.11 or newer, Flask, Flask-WTF, Flask-Limiter, SQLite, Bandit, pip-audit, Pytest, HTML, and CSS.

## Install on Windows PowerShell

Open PowerShell in this folder. The repository includes a local `.venv` in this workspace, but on a fresh checkout create one as shown:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If script activation is blocked, allow it for the current PowerShell process only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run the application

Set an application secret in the current PowerShell session. For local demonstrations, an omitted secret is generated randomly at startup; sessions then expire when the app restarts. Do not use that fallback for a deployed service.

```powershell
$env:SECRET_KEY = [Convert]::ToBase64String([Security.Cryptography.RandomNumberGenerator]::GetBytes(48))
python app.py
```

Open `http://127.0.0.1:5000`. SQLite data is created under `instance/` and is ignored by Git. To use HTTPS, configure the server for HTTPS and set `$env:COOKIE_SECURE = "true"`; keep it false for localhost HTTP.

## Security scan

Run Bandit against the application code:

```powershell
python -m bandit -f txt -o reports\final_scan.txt app.py database.py
```

The historical initial scan is preserved in `reports/initial_scan.txt`, with the scanned vulnerable source saved as `reports/initial_app.py`. Reproduce it with:

```powershell
python -m bandit -f txt -o reports\initial_scan.txt reports\initial_app.py
```

The final application scan output is `reports/final_scan.txt`. The command targets the two application Python modules directly, so it does not scan the virtual environment, tests, report snapshots, or database files.

## Tests

```powershell
python -m pytest tests -q
```

## Dependency audit

Check installed dependency versions against known vulnerability advisories:

```powershell
python -m pip_audit -r requirements.txt --format columns --cache-dir .pip-audit-cache --output reports\dependency_audit.txt
```

This command needs network access to query the package advisory service. A network or certificate error means the audit did not complete; it is not a clean result.

## Project layout

```text
Secure-Coding-Review/
├── app.py, database.py
├── requirements.txt, .env.example, .gitignore, pytest.ini
├── templates/                 # login, register, dashboard
├── static/style.css
├── tests/test_security.py
└── reports/                   # initial sample, scans, test output, audit report
```

## Reports

- `reports/initial_scan.txt`: real Bandit results for the intentionally vulnerable starting source.
- `reports/final_scan.txt`: real Bandit results after the fixes.
- `reports/test_results.txt`: actual Pytest output.
- `reports/security-review-report.md`: current review findings, fixes, recommendations, and retest results.
- `reports/dependency_audit.txt`: pip-audit result, when the advisory service is reachable.
- `reports/security_audit_report.md`: original Task 3 audit report and before/after Bandit review.

## Limitations

This is an educational localhost project, not production identity software. Login limiting uses in-memory storage by default, so request counters are not shared between multiple workers or restarts; Flask-Limiter cautions against in-memory storage for production ([configuration guidance](https://flask-limiter.readthedocs.io/en/stable/configuration.html)). Use shared Redis storage for a multi-worker deployment. There is no account lockout, password reset, email verification, MFA, account recovery, HTTPS termination, hardened deployment configuration, comprehensive security headers, or production database. Flask uses a signed client-side session. Use HTTPS and a managed secret, configure secure cookies, trust proxy headers only behind a trusted proxy, and obtain a professional review before deploying beyond local testing.
