# Test Report

## Automated tests

Command:

```bash
python3 -m unittest -v test_system.py
```

Result:

```text
Ran 93 tests
OK
```

| Category | Cases | Result |
|---|---:|---|
| Input validation | 17 | PASS |
| Authentication & persisted users | 10 | PASS |
| Password security & public signup | 10 | PASS |
| RBAC & event CRUD | 13 | PASS |
| Attendee registration | 14 | PASS |
| Search, reports & persistence | 22 | PASS |
| Automated reminders | 7 | PASS |
| **Total** | **93** | **PASS** |

Row-by-row details: `test_case_matrix.csv`.

## Manual acceptance coverage

`manual_acceptance_test_cases.csv` contains 24 scenarios covering:

- account creation and role restrictions;
- Admin CRUD and reports;
- Organizer ownership and attendee management;
- Student search/register/cancel/view;
- validation, capacity and duplicate registration;
- JSON reload/corruption;
- CSV export;
- automated reminders.

## CLI end-to-end

The clean-storage run exercised:

1. Organizer and Student/Visitor account creation.
2. Admin login, event creation and update.
3. Clearing/re-adding an optional description.
4. Organizer reminder and attendee registration.
5. Student reminder, filtered search and duplicate rejection.
6. Registered-event view and cancellation.
7. Admin attendee view, statistics, CSV export and event deletion.
8. Normal exit with status `0`.

Validation result: **17/17 runtime assertions PASS**, no traceback.

Evidence:

- `runtime_cli_e2e_transcript.txt`
- `runtime_validation_results.txt`
- `runtime_users_hashed.json`
- `runtime_events_after_delete.json`
- `runtime_event_report.csv`

## Corrupted-data startup

An invalid event entry was written to `events.json`. The app returned:

```text
[Lỗi hệ thống] Mỗi sự kiện trong dữ liệu phải là một object JSON.
```

It exited normally without a traceback. Evidence:
`runtime_corrupted_data_handling.txt`.

## Quality checks

```text
python3 -m py_compile: PASS
flake8: PASS
```

Combined unit + CLI source coverage, including branches: **90%**.
See `coverage_report.txt`.
