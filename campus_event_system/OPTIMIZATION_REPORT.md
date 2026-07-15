# Optimization Report

## Baseline

Bộ optimized source được cung cấp đã có:

- 76/76 tests PASS.
- PBKDF2 password hashing.
- 7-day reminders.
- CSV `status` column.
- Functional coverage đầy đủ theo Assignment Option 1.

## Final audit improvements

| Area | Improvement |
|---|---|
| Validation | Reject non-string usernames, boolean/decimal IDs |
| Persistence | Validate JSON object/list shapes and duplicate IDs |
| Referential integrity | Validate event Organizer and attendees against users |
| Reminder API | Validate non-negative window and reference date |
| Security | Remove Admin from public signup |
| Password input | Preserve significant whitespace |
| CLI update | Allow `-` to clear optional description |
| Error handling | Corrupted domain data exits without traceback |
| Tests | Expanded from 76 to 93 |
| Documentation | Regenerated all stale 63-test artifacts |

## Final verification

```text
Automated tests:             93/93 PASS
Manual acceptance matrix:   24 cases
CLI assertions:             17/17 PASS
py_compile:                 PASS
flake8:                     PASS
Branch-inclusive coverage:  90%
```

See `AUDIT_REPORT.md` and `documentation/` for the complete evidence.
