# Concert + Bob Remediation Demo: Task Tracker

A small Flask task tracker used as a baseline for an IBM Bob + IBM Concert dependency remediation demonstration.

> **WARNING: intentionally vulnerable dependencies.**
> `requirements.txt` deliberately pins old versions (`Flask==3.0.2`, `Werkzeug==3.0.2`, `requests==2.31.0`) that have known published advisories. This is for a software composition analysis (SCA) demo. **Do not deploy this application.** An affected dependency version does not by itself mean the application is exploitable. See [`docs/demo-plan.md`](docs/demo-plan.md).

## Features

- Add, list, complete, and delete tasks in the browser.
- SQLite storage using parameterized queries (`tasks.db`, created on first run).
- `GET /health` returns `{"status": "ok"}`.
- Synthetic seed data on first run.
- Binds to `127.0.0.1:5050` only, with debug mode disabled.
- No authentication, external services, or credentials.

## Setup

Python 3.12 is recommended.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

On macOS/Linux: `python3.12 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt`

## Run

```powershell
.\.venv\Scripts\python.exe run.py
```

Open http://127.0.0.1:5050 and check http://127.0.0.1:5050/health.

## Test

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Tests use a temporary database and never touch `tasks.db`.

## Files

| File | Purpose |
| --- | --- |
| `requirements.txt` | Intentionally old baseline pins (runtime) |
| `requirements-dev.txt` | Runtime plus test tooling (pytest) |
| `requirements.lock.txt` | Resolved runtime dependency set at baseline |
| `docs/demo-plan.md` | Demo workflow |

## Dependency audit

Keep scanners in a separate environment from the app:

```powershell
py -3.12 -m venv .venv-scan
.\.venv-scan\Scripts\python.exe -m pip install pip-audit
py -3.12 -m venv .venv-runtime
.\.venv-runtime\Scripts\python.exe -m pip install -r requirements.txt
.\.venv-scan\Scripts\pip-audit.exe --path .\.venv-runtime\Lib\site-packages -f json -o scan-output\pip-audit-report.json
```

`pip-audit` exits non-zero when vulnerabilities are found. That is expected for this baseline. Scan output is git-ignored.
