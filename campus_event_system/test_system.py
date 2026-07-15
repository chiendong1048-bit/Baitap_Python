"""Comprehensive requirement, boundary, permission, and persistence tests."""

import csv
import json
import os
import shutil
import tempfile
import unittest
from datetime import date, datetime
from unittest.mock import patch

from auth import AuthManager
from exceptions import (
    AuthenticationError,
    DuplicateRegistrationError,
    EventFullError,
    EventNotFoundError,
    PermissionDeniedError,
    UserNotFoundError,
    ValidationError,
)
from managers import EventManager
from models import (
    Event,
    StudentVisitor,
    clean_event_name,
    clean_full_name,
    clean_whitespace,
    user_from_dict,
    validate_date,
)
import main as cli
import security
import storage


ORIGINAL_PASSWORD_ITERATIONS = security._ITERATIONS


def setUpModule():
    # PBKDF2 is deliberately slow to resist brute-force attacks (good for
    # production). That same slowness would make ~300 test-user
    # registrations take tens of seconds, so the test run lowers the
    # iteration count once, globally, while keeping the real algorithm and
    # salting logic under test. security.py itself is untouched.
    security._ITERATIONS = 1_000


def tearDownModule():
    security._ITERATIONS = ORIGINAL_PASSWORD_ITERATIONS


class IsolatedStorageTestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="campus_event_test_")
        storage.DATA_DIR = os.path.join(self.test_dir, "data")
        storage.REPORTS_DIR = os.path.join(self.test_dir, "reports")
        storage.USERS_FILE = os.path.join(storage.DATA_DIR, "users.json")
        storage.EVENTS_FILE = os.path.join(storage.DATA_DIR, "events.json")

        self.auth = AuthManager()
        self.admin = self.auth.register("adminUser", "pass", "Admin User", "1")
        self.organizer = self.auth.register(
            "orgUser",
            "pass",
            "Organizer User",
            "2",
        )
        self.organizer2 = self.auth.register(
            "orgTwo",
            "pass",
            "Second Organizer",
            "2",
        )
        self.student = self.auth.register(
            "studentUser",
            "pass",
            "Student User",
            "3",
        )
        self.student2 = self.auth.register(
            "studentTwo",
            "pass",
            "Second Student",
            "3",
        )
        self.manager = EventManager(self.auth)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def create_event(self, **overrides):
        values = {
            "name": "AI Workshop",
            "date_str": "2026-09-01",
            "capacity": 2,
            "organizer_username": self.organizer.username,
            "description": "Campus technology workshop.",
        }
        values.update(overrides)
        return self.manager.create_event(self.admin, **values)


class TestInputValidation(IsolatedStorageTestCase):
    def test_whitespace_is_collapsed(self):
        self.assertEqual(clean_whitespace("  Campus   Event  "), "Campus Event")

    def test_vietnamese_full_name_is_title_cased(self):
        self.assertEqual(clean_full_name("  đồng   tố chiến "), "Đồng Tố Chiến")

    def test_hyphenated_and_apostrophe_names_are_allowed(self):
        self.assertEqual(
            clean_full_name("jean-pierre o'connor"),
            "Jean-Pierre O'Connor",
        )

    def test_full_name_rejects_digits(self):
        with self.assertRaises(ValidationError):
            clean_full_name("Nguyen Van A2")

    def test_event_keywords_are_normalized(self):
        self.assertEqual(
            clean_event_name("  đại hội ai fpt workshop "),
            "Đại Hội AI FPT Workshop",
        )

    def test_empty_event_name_is_rejected(self):
        with self.assertRaises(ValidationError):
            self.create_event(name="   ")

    def test_overlong_event_name_is_rejected(self):
        with self.assertRaises(ValidationError):
            self.create_event(name="A" * 101)

    def test_date_format_is_strict(self):
        for invalid in ("01-09-2026", "2026/09/01", "2026-9-1", ""):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValidationError):
                    validate_date(invalid)

    def test_impossible_calendar_date_is_rejected(self):
        with self.assertRaises(ValidationError):
            self.create_event(date_str="2026-02-30")

    def test_leap_day_is_accepted(self):
        event = self.create_event(date_str="2028-02-29")
        self.assertEqual(event.date_str, "2028-02-29")

    def test_capacity_must_be_integer(self):
        for invalid in ("abc", "2.5", None, True):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValidationError):
                    self.create_event(capacity=invalid)

    def test_capacity_boundaries(self):
        for invalid in (0, -1, 100_001):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValidationError):
                    self.create_event(capacity=invalid)
        event = self.create_event(capacity=100_000)
        self.assertEqual(event.capacity, 100_000)

    def test_common_description_punctuation_is_allowed(self):
        event = self.create_event(
            description="Room A-1: Python/C++, 09:00 (bring ID).",
        )
        self.assertIn("Python/C++", event.description)

    def test_overlong_description_is_rejected(self):
        with self.assertRaises(ValidationError):
            self.create_event(description="A" * 501)

    def test_event_id_must_be_positive_integer(self):
        for invalid in (0, -1, "abc", True, 1.5):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValidationError):
                    Event(
                        invalid,
                        "AI Workshop",
                        "2026-09-01",
                        10,
                        "orgUser",
                    )

    def test_user_id_must_be_positive_integer(self):
        for invalid in (True, 1.5):
            data = {
                "user_id": invalid,
                "username": "newUser",
                "password_hash": "salt$digest",
                "full_name": "New User",
                "role": "Student/Visitor",
            }
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValidationError):
                    user_from_dict(data)

    def test_username_must_be_text(self):
        data = {
            "user_id": 10,
            "username": 12345,
            "password_hash": "salt$digest",
            "full_name": "New User",
            "role": "Student/Visitor",
        }
        with self.assertRaises(ValidationError):
            user_from_dict(data)
        with self.assertRaises(ValidationError):
            self.auth.register(12345, "pass", "New User", "3")


class TestAuthentication(IsolatedStorageTestCase):
    def test_valid_login_returns_correct_subclass(self):
        user = self.auth.login("studentUser", "pass")
        self.assertIsInstance(user, StudentVisitor)

    def test_unknown_username_is_rejected(self):
        with self.assertRaises(AuthenticationError):
            self.auth.login("missing", "pass")

    def test_wrong_password_is_rejected(self):
        with self.assertRaises(AuthenticationError):
            self.auth.login("adminUser", "wrong")

    def test_duplicate_username_is_rejected(self):
        with self.assertRaises(ValidationError):
            self.auth.register("adminUser", "pass", "Another User", "3")

    def test_invalid_role_choice_is_rejected(self):
        with self.assertRaises(ValidationError):
            self.auth.register("newUser", "pass", "New User", "9")

    def test_invalid_username_characters_are_rejected(self):
        for invalid in ("john doe", "john@", "john_doe", ""):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValidationError):
                    self.auth.register(invalid, "pass", "John Doe", "3")

    def test_get_unknown_user_is_rejected(self):
        with self.assertRaises(UserNotFoundError):
            self.auth.get_user("missing")

    def test_unknown_persisted_role_is_rejected(self):
        data = {
            "user_id": 20,
            "username": "unknownRole",
            "password": "pass",
            "full_name": "Unknown Role",
            "role": "Super User",
        }
        with self.assertRaises(ValidationError):
            user_from_dict(data)

    def test_persisted_user_entry_must_be_an_object(self):
        with self.assertRaises(ValidationError):
            user_from_dict("invalid")

    def test_duplicate_persisted_user_ids_are_rejected(self):
        with open(storage.USERS_FILE, "r", encoding="utf-8") as file:
            users = json.load(file)
        duplicate = dict(users[-1])
        duplicate["username"] = "differentUser"
        users.append(duplicate)
        with open(storage.USERS_FILE, "w", encoding="utf-8") as file:
            json.dump(users, file)
        with self.assertRaises(RuntimeError):
            AuthManager()


class TestPasswordSecurity(IsolatedStorageTestCase):
    def test_hash_password_does_not_return_the_raw_password(self):
        hashed = security.hash_password("pass123")
        self.assertNotEqual(hashed, "pass123")
        self.assertIn("$", hashed)

    def test_hash_password_uses_a_random_salt_each_time(self):
        first = security.hash_password("pass123")
        second = security.hash_password("pass123")
        self.assertNotEqual(first, second)

    def test_verify_password_accepts_the_correct_password(self):
        hashed = security.hash_password("pass123")
        self.assertTrue(security.verify_password("pass123", hashed))

    def test_verify_password_rejects_the_wrong_password(self):
        hashed = security.hash_password("pass123")
        self.assertFalse(security.verify_password("wrong", hashed))

    def test_verify_password_fails_closed_on_malformed_stored_hash(self):
        self.assertFalse(security.verify_password("pass123", "not-a-valid-hash"))
        self.assertFalse(security.verify_password("pass123", None))

    def test_registered_users_are_not_persisted_in_plain_text(self):
        with open(storage.USERS_FILE, "r", encoding="utf-8") as file:
            content = file.read()
        self.assertNotIn('"pass"', content)
        self.assertIn("password_hash", content)

    def test_login_still_works_after_reload_from_hashed_storage(self):
        reloaded_auth = AuthManager()
        user = reloaded_auth.login("studentUser", "pass")
        self.assertEqual(user.username, "studentUser")

    def test_persisted_unhashed_password_field_is_rejected(self):
        data = {
            "user_id": 30,
            "username": "legacyUser",
            "password": "plaintext",
            "full_name": "Legacy User",
            "role": "Student/Visitor",
        }
        with self.assertRaises(ValidationError):
            user_from_dict(data)

    def test_password_prompt_preserves_significant_whitespace(self):
        with patch.object(cli, "prompt", return_value="  secret phrase  "):
            self.assertEqual(
                cli.prompt_password("Mật khẩu: "),
                "  secret phrase  ",
            )

    def test_public_registration_cannot_create_admin(self):
        def choose_role(_label, valid_choices):
            self.assertEqual(valid_choices, {"2", "3"})
            return "2"

        with (
            patch.object(
                cli,
                "prompt_nonempty",
                side_effect=["publicOrg", "Public Organizer"],
            ),
            patch.object(cli, "prompt_password", return_value="secret"),
            patch.object(cli, "prompt_choice", side_effect=choose_role),
            patch("builtins.print"),
        ):
            user = cli.do_register(self.auth)
        self.assertEqual(user.role_name(), "Event Organizer")


class TestEventPermissionsAndCrud(IsolatedStorageTestCase):
    def test_admin_can_create_event(self):
        event = self.create_event()
        self.assertEqual(event.event_id, 1)

    def test_non_admin_cannot_create_event(self):
        for actor in (self.organizer, self.student):
            with self.subTest(role=actor.role_name()):
                with self.assertRaises(PermissionDeniedError):
                    self.manager.create_event(
                        actor,
                        "AI Workshop",
                        "2026-09-01",
                        10,
                        self.organizer.username,
                    )

    def test_event_requires_existing_organizer(self):
        with self.assertRaises(UserNotFoundError):
            self.create_event(organizer_username="missing")

    def test_event_rejects_non_organizer_owner(self):
        with self.assertRaises(ValidationError):
            self.create_event(organizer_username=self.student.username)

    def test_admin_can_update_all_fields(self):
        event = self.create_event()
        updated = self.manager.update_event(
            self.admin,
            event.event_id,
            name="STEM Lab",
            date_str="2026-10-02",
            capacity=25,
            organizer_username=self.organizer2.username,
            description="New description.",
        )
        self.assertEqual(updated.name, "STEM Lab")
        self.assertEqual(updated.date_str, "2026-10-02")
        self.assertEqual(updated.capacity, 25)
        self.assertEqual(updated.organizer_username, self.organizer2.username)

    def test_invalid_update_is_atomic(self):
        event = self.create_event()
        with self.assertRaises(ValidationError):
            self.manager.update_event(
                self.admin,
                event.event_id,
                name="Changed Name",
                date_str="invalid",
            )
        unchanged = self.manager.get_event(event.event_id)
        self.assertEqual(unchanged.name, "AI Workshop")
        self.assertEqual(unchanged.date_str, "2026-09-01")

    def test_admin_can_clear_optional_description(self):
        event = self.create_event(description="Remove this description")
        updated = self.manager.update_event(
            self.admin,
            event.event_id,
            description="",
        )
        self.assertEqual(updated.description, "")

    def test_capacity_cannot_shrink_below_registration_count(self):
        event = self.create_event(capacity=2)
        self.manager.register_attendee(self.student, event.event_id)
        self.manager.register_attendee(self.student2, event.event_id)
        with self.assertRaises(ValidationError):
            self.manager.update_event(
                self.admin,
                event.event_id,
                capacity=1,
            )

    def test_non_admin_cannot_update_event(self):
        event = self.create_event()
        with self.assertRaises(PermissionDeniedError):
            self.manager.update_event(
                self.organizer,
                event.event_id,
                capacity=5,
            )

    def test_admin_can_delete_event(self):
        event = self.create_event()
        self.manager.delete_event(self.admin, event.event_id)
        with self.assertRaises(EventNotFoundError):
            self.manager.get_event(event.event_id)

    def test_non_admin_cannot_delete_event(self):
        event = self.create_event()
        with self.assertRaises(PermissionDeniedError):
            self.manager.delete_event(self.organizer, event.event_id)

    def test_get_event_accepts_numeric_string(self):
        event = self.create_event()
        self.assertIs(self.manager.get_event(str(event.event_id)), event)

    def test_get_event_rejects_invalid_or_unknown_id(self):
        with self.assertRaises(ValidationError):
            self.manager.get_event("abc")
        with self.assertRaises(EventNotFoundError):
            self.manager.get_event(999)


class TestRegistrationRules(IsolatedStorageTestCase):
    def test_student_can_register_self(self):
        event = self.create_event()
        self.manager.register_attendee(self.student, event.event_id)
        self.assertIn(self.student.username, event.registered_usernames)

    def test_registration_returns_confirmation_data(self):
        event = self.create_event()
        result = self.manager.register_attendee(self.student, event.event_id)
        self.assertIs(result, event)
        self.assertEqual(result.registered_count, 1)

    def test_duplicate_registration_is_rejected(self):
        event = self.create_event()
        self.manager.register_attendee(self.student, event.event_id)
        with self.assertRaises(DuplicateRegistrationError):
            self.manager.register_attendee(self.student, event.event_id)

    def test_full_event_is_rejected(self):
        event = self.create_event(capacity=1)
        self.manager.register_attendee(self.student, event.event_id)
        with self.assertRaises(EventFullError):
            self.manager.register_attendee(self.student2, event.event_id)

    def test_student_cannot_register_another_user(self):
        event = self.create_event()
        with self.assertRaises(PermissionDeniedError):
            self.manager.register_attendee(
                self.student,
                event.event_id,
                self.student2.username,
            )

    def test_organizer_can_register_student_for_owned_event(self):
        event = self.create_event()
        self.manager.register_attendee(
            self.organizer,
            event.event_id,
            self.student.username,
        )
        self.assertIn(self.student.username, event.registered_usernames)

    def test_organizer_can_unregister_student_from_owned_event(self):
        event = self.create_event()
        self.manager.register_attendee(self.student, event.event_id)
        self.manager.unregister_attendee(
            self.organizer,
            event.event_id,
            self.student.username,
        )
        self.assertNotIn(self.student.username, event.registered_usernames)

    def test_organizer_cannot_manage_another_organizers_event(self):
        event = self.create_event()
        with self.assertRaises(PermissionDeniedError):
            self.manager.register_attendee(
                self.organizer2,
                event.event_id,
                self.student.username,
            )

    def test_organizer_must_supply_attendee_username(self):
        event = self.create_event()
        with self.assertRaises(ValidationError):
            self.manager.register_attendee(self.organizer, event.event_id)

    def test_unknown_attendee_is_rejected(self):
        event = self.create_event()
        with self.assertRaises(UserNotFoundError):
            self.manager.register_attendee(
                self.organizer,
                event.event_id,
                "missing",
            )

    def test_non_student_attendee_is_rejected(self):
        event = self.create_event()
        with self.assertRaises(ValidationError):
            self.manager.register_attendee(
                self.organizer,
                event.event_id,
                self.admin.username,
            )

    def test_admin_cannot_bypass_registration_permissions(self):
        event = self.create_event()
        with self.assertRaises(PermissionDeniedError):
            self.manager.register_attendee(
                self.admin,
                event.event_id,
                self.student.username,
            )

    def test_student_can_unregister_self(self):
        event = self.create_event()
        self.manager.register_attendee(self.student, event.event_id)
        self.manager.unregister_attendee(self.student, event.event_id)
        self.assertNotIn(self.student.username, event.registered_usernames)

    def test_unregistering_absent_attendee_is_rejected(self):
        event = self.create_event()
        with self.assertRaises(ValidationError):
            self.manager.unregister_attendee(self.student, event.event_id)


class TestSearchReportsAndPersistence(IsolatedStorageTestCase):
    def test_search_finds_name_case_insensitively(self):
        self.create_event(name="AI Workshop")
        results = self.manager.search_events(keyword="ai")
        self.assertEqual([event.name for event in results], ["AI Workshop"])

    def test_search_finds_description(self):
        self.create_event(description="Robotics competition")
        results = self.manager.search_events(keyword="robotics")
        self.assertEqual(len(results), 1)

    def test_search_filters_by_valid_date(self):
        self.create_event(date_str="2026-09-01")
        self.create_event(name="STEM Lab", date_str="2026-09-02")
        results = self.manager.search_events(date_str="2026-09-02")
        self.assertEqual([event.name for event in results], ["STEM Lab"])

    def test_search_rejects_invalid_date_instead_of_silently_failing(self):
        with self.assertRaises(ValidationError):
            self.manager.search_events(date_str="02/09/2026")

    def test_only_available_filter_excludes_full_events(self):
        full_event = self.create_event(capacity=1)
        self.manager.register_attendee(self.student, full_event.event_id)
        open_event = self.create_event(name="Open Lab", date_str="2026-09-02")
        results = self.manager.search_events(only_available=True)
        self.assertEqual([event.event_id for event in results], [open_event.event_id])

    def test_attendee_can_view_registered_events(self):
        event = self.create_event()
        self.manager.register_attendee(self.student, event.event_id)
        self.assertEqual(
            self.manager.events_for_attendee(self.student.username),
            [event],
        )

    def test_total_attendees_counts_registrations_across_events(self):
        first = self.create_event()
        second = self.create_event(name="STEM Lab", date_str="2026-09-02")
        self.manager.register_attendee(self.student, first.event_id)
        self.manager.register_attendee(self.student, second.event_id)
        self.manager.register_attendee(self.student2, second.event_id)
        self.assertEqual(self.manager.total_attendees(), 3)

    def test_highest_and_lowest_report_all_ties(self):
        first = self.create_event()
        second = self.create_event(name="STEM Lab", date_str="2026-09-02")
        self.manager.register_attendee(self.student, first.event_id)
        self.manager.register_attendee(self.student2, second.event_id)
        report = self.manager.statistics_report()
        self.assertEqual(len(report["highest_events"]), 2)
        self.assertEqual(len(report["lowest_events"]), 2)

    def test_empty_statistics_report_is_safe(self):
        report = self.manager.statistics_report()
        self.assertEqual(report["total_events"], 0)
        self.assertEqual(report["total_attendees"], 0)
        self.assertEqual(report["highest_events"], [])
        self.assertEqual(report["lowest_events"], [])

    def test_users_and_events_survive_reload(self):
        event = self.create_event()
        self.manager.register_attendee(self.student, event.event_id)
        reloaded_auth = AuthManager()
        reloaded_manager = EventManager(reloaded_auth)
        reloaded = reloaded_manager.get_event(event.event_id)
        self.assertEqual(reloaded.registered_usernames, [self.student.username])
        self.assertEqual(len(reloaded_auth.users), len(self.auth.users))

    def test_corrupted_json_is_reported(self):
        os.makedirs(storage.DATA_DIR, exist_ok=True)
        with open(storage.EVENTS_FILE, "w", encoding="utf-8") as file:
            file.write("{not valid json")
        with self.assertRaises(RuntimeError):
            EventManager(self.auth)

    def test_non_list_json_root_is_reported(self):
        os.makedirs(storage.DATA_DIR, exist_ok=True)
        with open(storage.EVENTS_FILE, "w", encoding="utf-8") as file:
            json.dump({"event_id": 1}, file)
        with self.assertRaises(RuntimeError):
            EventManager(self.auth)

    def test_duplicate_persisted_registrations_are_rejected(self):
        data = {
            "event_id": 1,
            "name": "AI Workshop",
            "date": "2026-09-01",
            "capacity": 2,
            "organizer_username": self.organizer.username,
            "description": "",
            "registered_usernames": [self.student.username, self.student.username],
        }
        os.makedirs(storage.DATA_DIR, exist_ok=True)
        with open(storage.EVENTS_FILE, "w", encoding="utf-8") as file:
            json.dump([data], file)
        with self.assertRaises(ValidationError):
            EventManager(self.auth)

    def test_persisted_registration_collection_must_be_a_list(self):
        data = self.create_event().to_dict()
        data["registered_usernames"] = self.student.username
        with open(storage.EVENTS_FILE, "w", encoding="utf-8") as file:
            json.dump([data], file)
        with self.assertRaises(ValidationError):
            EventManager(self.auth)

    def test_persisted_registration_username_must_be_text(self):
        data = self.create_event().to_dict()
        data["registered_usernames"] = [12345]
        with open(storage.EVENTS_FILE, "w", encoding="utf-8") as file:
            json.dump([data], file)
        with self.assertRaises(ValidationError):
            EventManager(self.auth)

    def test_persisted_event_entry_must_be_an_object(self):
        with open(storage.EVENTS_FILE, "w", encoding="utf-8") as file:
            json.dump(["invalid"], file)
        with self.assertRaises(ValidationError):
            EventManager(self.auth)

    def test_duplicate_persisted_event_ids_are_rejected(self):
        first = self.create_event().to_dict()
        second = dict(first)
        second["name"] = "Second Event"
        with open(storage.EVENTS_FILE, "w", encoding="utf-8") as file:
            json.dump([first, second], file)
        with self.assertRaises(RuntimeError):
            EventManager(self.auth)

    def test_persisted_event_requires_existing_organizer(self):
        data = self.create_event().to_dict()
        data["organizer_username"] = "missingOrg"
        with open(storage.EVENTS_FILE, "w", encoding="utf-8") as file:
            json.dump([data], file)
        with self.assertRaises(ValidationError):
            EventManager(self.auth)

    def test_persisted_attendee_must_be_student_or_visitor(self):
        data = self.create_event().to_dict()
        data["registered_usernames"] = [self.admin.username]
        with open(storage.EVENTS_FILE, "w", encoding="utf-8") as file:
            json.dump([data], file)
        with self.assertRaises(ValidationError):
            EventManager(self.auth)

    def test_csv_export_contains_expected_columns_and_utf8_bom(self):
        event = self.create_event(name="Sự Kiện AI")
        self.manager.register_attendee(self.student, event.event_id)
        path = self.manager.export_statistics_csv()
        with open(path, "rb") as file:
            self.assertTrue(file.read(3).startswith(b"\xef\xbb\xbf"))
        with open(path, "r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(rows[0]["name"], "Sự Kiện AI")
        self.assertEqual(rows[0]["attendees"], self.student.username)

    def test_csv_export_reports_seat_status_in_vietnamese(self):
        full_event = self.create_event(capacity=1)
        self.manager.register_attendee(self.student, full_event.event_id)
        open_event = self.create_event(name="Open Lab", date_str="2026-09-02")
        path = self.manager.export_statistics_csv()
        with open(path, "r", encoding="utf-8-sig", newline="") as file:
            rows = {row["event_id"]: row["status"] for row in csv.DictReader(file)}
        self.assertEqual(rows[str(full_event.event_id)], "Hết chỗ")
        self.assertEqual(rows[str(open_event.event_id)], "Còn chỗ")

    def test_csv_export_rejects_path_traversal(self):
        with self.assertRaises(ValueError):
            storage.export_csv("../report.csv", ["event_id"], [])


class TestUpcomingEventReminders(IsolatedStorageTestCase):
    def test_attendee_reminder_includes_event_within_window(self):
        event = self.create_event(date_str="2026-09-01")
        self.manager.register_attendee(self.student, event.event_id)
        upcoming = self.manager.upcoming_events_for_attendee(
            self.student.username, within_days=7, today=date(2026, 8, 28)
        )
        self.assertEqual(upcoming, [event])

    def test_attendee_reminder_excludes_event_far_in_the_future(self):
        event = self.create_event(date_str="2026-09-01")
        self.manager.register_attendee(self.student, event.event_id)
        upcoming = self.manager.upcoming_events_for_attendee(
            self.student.username, within_days=7, today=date(2026, 8, 1)
        )
        self.assertEqual(upcoming, [])

    def test_attendee_reminder_excludes_event_already_in_the_past(self):
        event = self.create_event(date_str="2026-09-01")
        self.manager.register_attendee(self.student, event.event_id)
        upcoming = self.manager.upcoming_events_for_attendee(
            self.student.username, within_days=7, today=date(2026, 9, 5)
        )
        self.assertEqual(upcoming, [])

    def test_organizer_reminder_only_covers_their_own_events(self):
        owned = self.create_event(date_str="2026-09-01")
        self.create_event(
            name="Other Lab",
            date_str="2026-09-01",
            organizer_username=self.organizer2.username,
        )
        upcoming = self.manager.upcoming_events_for_organizer(
            self.organizer.username, within_days=7, today=date(2026, 8, 30)
        )
        self.assertEqual(upcoming, [owned])

    def test_reminder_window_must_be_non_negative_integer(self):
        for invalid in (-1, True, "abc"):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValidationError):
                    self.manager.upcoming_events_for_attendee(
                        self.student.username,
                        within_days=invalid,
                        today=date(2026, 8, 30),
                    )

    def test_reminder_accepts_datetime_reference(self):
        event = self.create_event(date_str="2026-09-01")
        self.manager.register_attendee(self.student, event.event_id)
        upcoming = self.manager.upcoming_events_for_attendee(
            self.student.username,
            within_days=7,
            today=datetime(2026, 8, 30, 12, 0),
        )
        self.assertEqual(upcoming, [event])

    def test_reminder_rejects_invalid_reference_date(self):
        with self.assertRaises(ValidationError):
            self.manager.upcoming_events_for_attendee(
                self.student.username,
                within_days=7,
                today="2026-08-30",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
