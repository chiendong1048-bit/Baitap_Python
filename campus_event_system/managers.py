"""Business rules for events, permissions, registrations, and reports."""

from datetime import date, datetime, timedelta

from exceptions import (
    CampusEventError,
    DuplicateRegistrationError,
    EventFullError,
    EventNotFoundError,
    PermissionDeniedError,
    ValidationError,
)
from models import (
    Admin,
    DATE_FORMAT,
    Event,
    Organizer,
    StudentVisitor,
    clean_whitespace,
    validate_date,
)
import storage

DEFAULT_REMINDER_WINDOW_DAYS = 7


class EventManager:
    def __init__(self, auth_manager=None):
        self.auth_manager = auth_manager
        self.events = {}
        self._next_id = 1
        self._load()

    def _load(self):
        raw_events = storage.load_events()
        for item in raw_events:
            event = Event.from_dict(item)
            if event.event_id in self.events:
                raise RuntimeError(
                    f"Dữ liệu chứa Event ID trùng lặp: {event.event_id}."
                )
            self._validate_loaded_event_users(event)
            self.events[event.event_id] = event
        if self.events:
            self._next_id = max(self.events) + 1

    def save(self):
        events = sorted(self.events.values(), key=lambda event: event.event_id)
        storage.save_events([event.to_dict() for event in events])

    def create_event(
        self,
        actor,
        name,
        date_str,
        capacity,
        organizer_username,
        description="",
    ):
        self._require_role(actor, Admin, "tạo sự kiện")
        organizer_username = self._get_organizer_username(organizer_username)
        event = Event(
            self._next_id,
            name,
            date_str,
            capacity,
            organizer_username,
            description,
        )
        self.events[event.event_id] = event
        self._next_id += 1
        self.save()
        return event

    def update_event(self, actor, event_id, **fields):
        self._require_role(actor, Admin, "cập nhật sự kiện")
        current = self.get_event(event_id)
        organizer_username = self._get_organizer_username(
            fields.get("organizer_username", current.organizer_username)
        )
        updated = Event(
            current.event_id,
            fields.get("name", current.name),
            fields.get("date_str", current.date_str),
            fields.get("capacity", current.capacity),
            organizer_username,
            fields.get("description", current.description),
        )
        if updated.capacity < current.registered_count:
            raise ValidationError(
                f"Không thể giảm sức chứa xuống {updated.capacity}; "
                f"đã có {current.registered_count} người đăng ký."
            )
        updated.registered_usernames = list(current.registered_usernames)
        self.events[current.event_id] = updated
        self.save()
        return updated

    def delete_event(self, actor, event_id):
        self._require_role(actor, Admin, "xóa sự kiện")
        event = self.get_event(event_id)
        del self.events[event.event_id]
        self.save()

    def get_event(self, event_id):
        normalized_id = self._normalize_event_id(event_id)
        event = self.events.get(normalized_id)
        if event is None:
            raise EventNotFoundError(
                f"Không tìm thấy sự kiện có ID {normalized_id}."
            )
        return event

    def list_all_events(self):
        return sorted(
            self.events.values(),
            key=lambda event: (event.date_str, event.event_id),
        )

    def list_events_for_organizer(self, organizer_username):
        username = clean_whitespace(organizer_username)
        return [
            event
            for event in self.list_all_events()
            if event.organizer_username == username
        ]

    def search_events(self, keyword=None, date_str=None, only_available=False):
        results = self.list_all_events()
        normalized_keyword = clean_whitespace(keyword).casefold()
        if normalized_keyword:
            results = [
                event
                for event in results
                if normalized_keyword in event.name.casefold()
                or normalized_keyword in event.description.casefold()
            ]
        normalized_date = clean_whitespace(date_str)
        if normalized_date:
            normalized_date = validate_date(normalized_date)
            results = [
                event for event in results if event.date_str == normalized_date
            ]
        if only_available:
            results = [event for event in results if not event.is_full]
        return results

    def register_attendee(self, actor, event_id, username=None):
        event = self.get_event(event_id)
        attendee = self._resolve_registration_target(actor, event, username)
        if attendee.username in event.registered_usernames:
            raise DuplicateRegistrationError(
                f"'{attendee.username}' đã đăng ký sự kiện '{event.name}'."
            )
        if event.is_full:
            raise EventFullError(
                f"Sự kiện '{event.name}' đã đủ {event.capacity} người."
            )
        event.registered_usernames.append(attendee.username)
        self.save()
        return event

    def unregister_attendee(self, actor, event_id, username=None):
        event = self.get_event(event_id)
        attendee = self._resolve_registration_target(actor, event, username)
        if attendee.username not in event.registered_usernames:
            raise ValidationError(
                f"'{attendee.username}' chưa đăng ký sự kiện '{event.name}'."
            )
        event.registered_usernames.remove(attendee.username)
        self.save()
        return event

    def events_for_attendee(self, username):
        normalized_username = clean_whitespace(username)
        return [
            event
            for event in self.list_all_events()
            if normalized_username in event.registered_usernames
        ]

    def _events_within_window(self, events, within_days, today):
        if isinstance(within_days, bool):
            raise ValidationError("Số ngày nhắc lịch phải là số nguyên không âm.")
        try:
            normalized_days = int(str(within_days).strip())
        except (TypeError, ValueError) as error:
            raise ValidationError(
                "Số ngày nhắc lịch phải là số nguyên không âm."
            ) from error
        if normalized_days < 0:
            raise ValidationError("Số ngày nhắc lịch phải là số nguyên không âm.")

        if today is None:
            reference = date.today()
        elif isinstance(today, datetime):
            reference = today.date()
        elif isinstance(today, date):
            reference = today
        else:
            raise ValidationError("Ngày tham chiếu nhắc lịch không hợp lệ.")

        horizon = reference + timedelta(days=normalized_days)
        upcoming = []
        for event in events:
            event_date = datetime.strptime(event.date_str, DATE_FORMAT).date()
            if reference <= event_date <= horizon:
                upcoming.append(event)
        return upcoming

    def upcoming_events_for_attendee(
        self, username, within_days=DEFAULT_REMINDER_WINDOW_DAYS, today=None
    ):
        """Events the given attendee is registered for in the next N days.

        Automated reminder used at login so a Student/Visitor never misses an
        event they signed up for.
        """
        return self._events_within_window(
            self.events_for_attendee(username), within_days, today
        )

    def upcoming_events_for_organizer(
        self, organizer_username, within_days=DEFAULT_REMINDER_WINDOW_DAYS, today=None
    ):
        """Events the given organizer owns that are happening in the next N days."""
        return self._events_within_window(
            self.list_events_for_organizer(organizer_username), within_days, today
        )

    def total_attendees(self):
        return sum(event.registered_count for event in self.events.values())

    def events_with_highest_attendance(self):
        if not self.events:
            return []
        highest_count = max(
            event.registered_count for event in self.events.values()
        )
        return [
            event
            for event in self.list_all_events()
            if event.registered_count == highest_count
        ]

    def events_with_lowest_attendance(self):
        if not self.events:
            return []
        lowest_count = min(
            event.registered_count for event in self.events.values()
        )
        return [
            event
            for event in self.list_all_events()
            if event.registered_count == lowest_count
        ]

    def event_with_highest_attendance(self):
        events = self.events_with_highest_attendance()
        return events[0] if events else None

    def event_with_lowest_attendance(self):
        events = self.events_with_lowest_attendance()
        return events[0] if events else None

    def statistics_report(self):
        highest_events = self.events_with_highest_attendance()
        lowest_events = self.events_with_lowest_attendance()
        return {
            "total_events": len(self.events),
            "total_attendees": self.total_attendees(),
            "highest": highest_events[0] if highest_events else None,
            "lowest": lowest_events[0] if lowest_events else None,
            "highest_events": highest_events,
            "lowest_events": lowest_events,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    def export_statistics_csv(self):
        rows = [
            {
                "event_id": event.event_id,
                "name": event.name,
                "date": event.date_str,
                "organizer": event.organizer_username,
                "capacity": event.capacity,
                "registered": event.registered_count,
                "seats_left": event.seats_left,
                "status": "Hết chỗ" if event.is_full else "Còn chỗ",
                "attendees": "; ".join(event.registered_usernames),
            }
            for event in self.list_all_events()
        ]
        headers = [
            "event_id",
            "name",
            "date",
            "organizer",
            "capacity",
            "registered",
            "seats_left",
            "status",
            "attendees",
        ]
        filename = f"event_report_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.csv"
        return storage.export_csv(filename, headers, rows)

    def _get_organizer_username(self, username):
        if self.auth_manager is None:
            raise RuntimeError(
                "EventManager cần AuthManager để xác minh Event Organizer."
            )
        user = self.auth_manager.get_user(username)
        if not isinstance(user, Organizer):
            raise ValidationError(
                f"Tài khoản '{user.username}' không phải Event Organizer."
            )
        return user.username

    def _validate_loaded_event_users(self, event):
        if self.auth_manager is None:
            return
        try:
            organizer = self.auth_manager.get_user(event.organizer_username)
            if not isinstance(organizer, Organizer):
                raise ValidationError(
                    f"Organizer '{event.organizer_username}' không đúng vai trò."
                )
            for username in event.registered_usernames:
                attendee = self.auth_manager.get_user(username)
                if not isinstance(attendee, StudentVisitor):
                    raise ValidationError(
                        f"Người tham gia '{username}' không phải Student/Visitor."
                    )
        except CampusEventError as error:
            raise ValidationError(
                f"Dữ liệu sự kiện ID {event.event_id} tham chiếu tài khoản "
                f"không hợp lệ: {error}"
            ) from error

    def _resolve_registration_target(self, actor, event, username):
        if isinstance(actor, StudentVisitor):
            target_username = clean_whitespace(username) or actor.username
            if target_username != actor.username:
                raise PermissionDeniedError(
                    "Student/Visitor chỉ được đăng ký hoặc hủy đăng ký cho chính mình."
                )
        elif isinstance(actor, Organizer):
            if actor.username != event.organizer_username:
                raise PermissionDeniedError(
                    "Organizer chỉ được quản lý đăng ký cho sự kiện của mình."
                )
            target_username = clean_whitespace(username)
            if not target_username:
                raise ValidationError("Cần nhập username người tham gia.")
        else:
            raise PermissionDeniedError(
                "Chỉ Student/Visitor hoặc Organizer phụ trách sự kiện "
                "được quản lý đăng ký."
            )

        if self.auth_manager is None:
            if target_username == actor.username and isinstance(actor, StudentVisitor):
                return actor
            raise ValidationError(
                "Không thể xác minh người tham gia khi thiếu AuthManager."
            )
        attendee = self.auth_manager.get_user(target_username)
        if not isinstance(attendee, StudentVisitor):
            raise ValidationError(
                "Người tham gia phải có vai trò Student/Visitor."
            )
        return attendee

    @staticmethod
    def _normalize_event_id(event_id):
        if isinstance(event_id, bool):
            raise ValidationError("Event ID phải là số nguyên dương.")
        try:
            normalized_id = int(str(event_id).strip())
        except (TypeError, ValueError) as error:
            raise ValidationError("Event ID phải là số nguyên dương.") from error
        if normalized_id <= 0:
            raise ValidationError("Event ID phải là số nguyên dương.")
        return normalized_id

    @staticmethod
    def _require_role(actor, role_class, action):
        if not isinstance(actor, role_class):
            raise PermissionDeniedError(
                f"Chỉ {role_class.__name__} được {action}; "
                f"vai trò hiện tại: {actor.role_name()}."
            )
