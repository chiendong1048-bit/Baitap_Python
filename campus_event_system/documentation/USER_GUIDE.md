# User Guide

## Start

```bash
python3 main.py
```

Default Admin:

```text
admin / admin123
```

## Create accounts

Choose `2. Đăng ký tài khoản`.

Public roles:

- `2` Event Organizer
- `3` Student/Visitor

Admin accounts cannot be created through public signup.

## Admin workflow

1. Login as Admin.
2. Create Organizer accounts before assigning an event.
3. Use:
   - `1` view all events;
   - `2` create;
   - `3` update;
   - `4` delete;
   - `5` view attendees;
   - `6` statistics;
   - `7` CSV export.
4. During update, leave a field blank to keep it. Enter `-` for description
   to clear the optional description.

## Event Organizer workflow

1. Login with an Organizer account.
2. Upcoming owned events within seven days are shown automatically.
3. Use `1` to view owned events and attendee details.
4. Use `2` to add/cancel a Student/Visitor registration.

An Organizer cannot manage an event assigned to another Organizer.

## Student/Visitor workflow

1. Login with a Student/Visitor account.
2. Upcoming registered events within seven days are shown automatically.
3. Use `1` to search by keyword/date and optionally filter available seats.
4. Use `2` to register.
5. Use `3` to cancel.
6. Use `4` to view registered events.

Student/Visitor can only manage their own registrations.

## Generated data

```text
data/users.json
data/events.json
reports/event_report_*.csv
```

Deleting these runtime folders resets local demo data. They are ignored by Git.
