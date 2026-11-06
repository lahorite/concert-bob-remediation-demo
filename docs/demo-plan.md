# Demo Plan

Workflow: baseline → scan → Concert ingestion → Bob remediation → tests → rescan → verification.

## 1. Baseline

- Flask task tracker with intentionally old pins: `Flask==3.0.2`, `Werkzeug==3.0.2`, `requests==2.31.0`.
- Functional tests pass; `requirements.lock.txt` records the resolved runtime set.
- **Exit criteria:** tests green, baseline committed locally, no remediation applied.

## 2. Scan

- Run `pip-audit` from a separate scanner environment against the app's runtime environment.
- Save the machine-readable report (`scan-output/pip-audit-report.json`, git-ignored).
- Findings are expected and are not functional test failures.

## 3. Concert ingestion

- Configure the Concert data connection and import the scan results (configured in a later phase).
- Confirm the findings appear in Concert before any remediation. Do not claim ingestion until it is observed.

## 4. Bob remediation

- Use Bob to plan and apply dependency upgrades on a fresh branch.
- Choose target versions from advisory fix versions, staying within the same major version where possible.
- Change only the in-scope packages and update `requirements.txt` and `requirements.lock.txt`.

## 5. Tests

- Rebuild the environment from the updated pins.
- Run the functional test suite and confirm `/health` and task CRUD still pass.

## 6. Rescan

- Re-run the same `pip-audit` command against a freshly built runtime environment.
- Re-ingest the new results into Concert.

## 7. Verification

- Compare before and after findings by advisory ID.
- Record anything still open and why.
- Separate "affected version removed" from "exploitable in this application". The two are not the same claim.
- Review the diff to confirm only intended files changed.
