---
name: testing-campus-event-cli
description: Test the Campus Event Management System CLI end-to-end across Admin, Organizer, and Student/Visitor roles.
---

# Campus Event CLI testing

## Devin Secrets Needed

None. The application is local and uses JSON files under `campus_event_system/data/`.

## Setup

1. Work from the repository root, then enter `campus_event_system/`.
2. For a deterministic clean run, remove the ignored `data/` and `reports/`
   directories before starting.
3. Run:

   ```bash
   python3 main.py
   ```

4. The app seeds the local demo Admin account `admin` / `admin123`.
5. Usernames must be alphanumeric; underscores and spaces are intentionally rejected.

## Role access

- Admin: event CRUD, attendee views, statistics, and CSV export.
- Organizer: event views and attendee management only for owned events.
- Student/Visitor: event search and self-registration/cancellation.

Create Organizer and Student/Visitor accounts in the CLI before assigning an event.

## High-value end-to-end flow

1. Register one Organizer and one Student/Visitor.
2. Log in as Admin and create a capacity-one event assigned to the Organizer.
3. Log in as Organizer, add the Student/Visitor, and verify the event becomes `1/1`.
4. Log in as Student/Visitor, search by description/date, and verify the real event ID
   is shown without a traceback.
5. Attempt a duplicate registration and verify it is rejected while the menu remains active.
6. View the registered event, cancel it, and verify the registered-event count becomes zero.
7. Log in as Admin, verify statistics, export CSV, and exit normally.

## Persistence checks

- `data/users.json`: expected usernames and role names.
- `data/events.json`: event ID, organizer, capacity, and final registration list.
- `reports/*.csv`: one row per event with `registered`, `seats_left`, and attendees.
- Verify no `Traceback` appears in the captured CLI transcript.

## Automated checks

```bash
python3 -m unittest -v test_system.py
python3 -m py_compile auth.py exceptions.py main.py managers.py models.py storage.py test_system.py
flake8 --max-line-length=88 auth.py exceptions.py main.py managers.py models.py storage.py test_system.py
```
