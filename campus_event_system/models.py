"""Domain models and validation for the campus event system."""

import re
from abc import ABC, abstractmethod
from datetime import datetime

from exceptions import ValidationError


KEYWORD_MAP = {
    "AI": "AI",
    "API": "API",
    "FPT": "FPT",
    "IT": "IT",
    "LAB": "Lab",
    "STEM": "STEM",
    "UI": "UI",
    "UX": "UX",
    "WORKSHOP": "Workshop",
}
DATE_FORMAT = "%Y-%m-%d"
MAX_EVENT_CAPACITY = 100_000
MAX_EVENT_NAME_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 500
MAX_USERNAME_LENGTH = 30


def clean_whitespace(value):
    """Trim a value and collapse consecutive whitespace."""
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def validate_username(username):
    """Return a normalized alphanumeric username."""
    if not isinstance(username, str):
        raise ValidationError("Username phải là chuỗi ký tự.")
    cleaned = clean_whitespace(username)
    if not cleaned or not cleaned.isalnum():
        raise ValidationError(
            "Username chỉ được chứa chữ cái và chữ số, không có khoảng trắng."
        )
    if len(cleaned) > MAX_USERNAME_LENGTH:
        raise ValidationError(
            f"Username không được vượt quá {MAX_USERNAME_LENGTH} ký tự."
        )
    return cleaned


def clean_full_name(name):
    """Validate and title-case a person's name."""
    cleaned = clean_whitespace(name)
    if not cleaned:
        raise ValidationError("Họ và tên không được để trống.")
    if len(cleaned) > 100:
        raise ValidationError("Họ và tên không được vượt quá 100 ký tự.")
    if not all(char.isalpha() or char in " -'" for char in cleaned):
        raise ValidationError(
            "Họ và tên chỉ được chứa chữ cái, khoảng trắng, dấu nháy hoặc dấu gạch nối."
        )
    return cleaned.title()


def clean_event_name(name):
    """Validate and normalize an event name."""
    cleaned = clean_whitespace(name)
    if not cleaned:
        raise ValidationError("Tên sự kiện không được để trống.")
    if len(cleaned) > MAX_EVENT_NAME_LENGTH:
        raise ValidationError(
            f"Tên sự kiện không được vượt quá {MAX_EVENT_NAME_LENGTH} ký tự."
        )
    if not any(char.isalnum() for char in cleaned):
        raise ValidationError("Tên sự kiện phải chứa ít nhất một chữ cái hoặc chữ số.")

    words = []
    for word in cleaned.split():
        prefix = ""
        suffix = ""
        core = word
        while core and not core[0].isalnum():
            prefix += core[0]
            core = core[1:]
        while core and not core[-1].isalnum():
            suffix = core[-1] + suffix
            core = core[:-1]
        normalized = KEYWORD_MAP.get(core.upper(), core.capitalize())
        words.append(prefix + normalized + suffix)
    return " ".join(words)


def validate_date(date_str):
    """Return a normalized YYYY-MM-DD date or raise ValidationError."""
    cleaned = clean_whitespace(date_str)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", cleaned):
        raise ValidationError(
            "Ngày phải đúng định dạng YYYY-MM-DD, ví dụ 2026-05-29."
        )
    try:
        parsed = datetime.strptime(cleaned, DATE_FORMAT)
    except ValueError as error:
        raise ValidationError("Ngày không tồn tại trên lịch.") from error
    return parsed.strftime(DATE_FORMAT)


class User(ABC):
    """Base class for authenticated users."""

    def __init__(self, user_id, username, password_hash, full_name):
        cleaned_username = validate_username(username)
        if not password_hash or not str(password_hash).strip():
            raise ValidationError(
                "Dữ liệu mật khẩu đã băm không được để trống."
            )

        if isinstance(user_id, bool):
            raise ValidationError("User ID phải là số nguyên dương.")
        try:
            normalized_id = int(str(user_id).strip())
        except (TypeError, ValueError) as error:
            raise ValidationError("User ID phải là số nguyên dương.") from error
        if normalized_id <= 0:
            raise ValidationError("User ID phải là số nguyên dương.")

        self.user_id = normalized_id
        self.username = cleaned_username
        self.password_hash = str(password_hash)
        self.full_name = clean_full_name(full_name)

    @abstractmethod
    def role_name(self):
        """Return the stored role name."""

    @abstractmethod
    def menu_options(self):
        """Return role-specific menu entries."""

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password_hash": self.password_hash,
            "full_name": self.full_name,
            "role": self.role_name(),
        }


class Admin(User):
    def role_name(self):
        return "Admin"

    def menu_options(self):
        return [
            ("1", "Xem tất cả sự kiện"),
            ("2", "Tạo sự kiện"),
            ("3", "Cập nhật sự kiện"),
            ("4", "Xóa sự kiện"),
            ("5", "Xem người tham gia"),
            ("6", "Xem báo cáo thống kê"),
            ("7", "Xuất báo cáo CSV"),
            ("0", "Đăng xuất"),
        ]


class Organizer(User):
    def role_name(self):
        return "Event Organizer"

    def menu_options(self):
        return [
            ("1", "Xem chi tiết sự kiện của tôi"),
            ("2", "Quản lý đăng ký người tham gia"),
            ("0", "Đăng xuất"),
        ]


class StudentVisitor(User):
    def role_name(self):
        return "Student/Visitor"

    def menu_options(self):
        return [
            ("1", "Tìm kiếm sự kiện"),
            ("2", "Đăng ký sự kiện"),
            ("3", "Hủy đăng ký"),
            ("4", "Xem sự kiện đã đăng ký"),
            ("0", "Đăng xuất"),
        ]


ROLE_CLASS_MAP = {
    "Admin": Admin,
    "Event Organizer": Organizer,
    "Student/Visitor": StudentVisitor,
}


def user_from_dict(data):
    """Deserialize a user while rejecting unknown persisted roles."""
    if not isinstance(data, dict):
        raise ValidationError("Mỗi người dùng trong dữ liệu phải là một object JSON.")
    try:
        role = data["role"]
        role_class = ROLE_CLASS_MAP[role]
        return role_class(
            data["user_id"],
            data["username"],
            data["password_hash"],
            data["full_name"],
        )
    except KeyError as error:
        field = error.args[0]
        if field == "role" and data.get("role") not in ROLE_CLASS_MAP:
            raise ValidationError(
                f"Vai trò lưu trong dữ liệu không hợp lệ: {data.get('role')!r}."
            ) from error
        raise ValidationError(f"Dữ liệu người dùng thiếu trường '{field}'.") from error


class Event:
    """A campus event with capacity and attendee tracking."""

    def __init__(
        self,
        event_id,
        name,
        date_str,
        capacity,
        organizer_username,
        description="",
    ):
        if isinstance(event_id, bool):
            raise ValidationError("Event ID phải là số nguyên dương.")
        try:
            normalized_id = int(str(event_id).strip())
        except (TypeError, ValueError) as error:
            raise ValidationError("Event ID phải là số nguyên dương.") from error
        if normalized_id <= 0:
            raise ValidationError("Event ID phải là số nguyên dương.")

        organizer = clean_whitespace(organizer_username)
        if not organizer:
            raise ValidationError("Organizer username không được để trống.")

        self.event_id = normalized_id
        self.name = clean_event_name(name)
        self.date_str = validate_date(date_str)
        self.capacity = self._validate_capacity(capacity)
        self.organizer_username = organizer
        self.description = self._validate_description(description)
        self.registered_usernames = []

    @staticmethod
    def _validate_capacity(capacity):
        if isinstance(capacity, bool):
            raise ValidationError("Sức chứa phải là số nguyên.")
        try:
            normalized = int(str(capacity).strip())
        except (TypeError, ValueError) as error:
            raise ValidationError("Sức chứa phải là số nguyên.") from error
        if normalized <= 0:
            raise ValidationError("Sức chứa phải lớn hơn 0.")
        if normalized > MAX_EVENT_CAPACITY:
            raise ValidationError(
                f"Sức chứa tối đa là {MAX_EVENT_CAPACITY:,} người."
            )
        return normalized

    @staticmethod
    def _validate_description(description):
        cleaned = clean_whitespace(description)
        if len(cleaned) > MAX_DESCRIPTION_LENGTH:
            raise ValidationError(
                f"Mô tả không được vượt quá {MAX_DESCRIPTION_LENGTH} ký tự."
            )
        if any(not char.isprintable() for char in cleaned):
            raise ValidationError("Mô tả chứa ký tự điều khiển không hợp lệ.")
        return cleaned

    @property
    def registered_count(self):
        return len(self.registered_usernames)

    @property
    def seats_left(self):
        return self.capacity - self.registered_count

    @property
    def is_full(self):
        return self.seats_left == 0

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "name": self.name,
            "date": self.date_str,
            "capacity": self.capacity,
            "organizer_username": self.organizer_username,
            "description": self.description,
            "registered_usernames": list(self.registered_usernames),
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValidationError("Mỗi sự kiện trong dữ liệu phải là một object JSON.")
        try:
            event = cls(
                data["event_id"],
                data["name"],
                data["date"],
                data["capacity"],
                data["organizer_username"],
                data.get("description", ""),
            )
            raw_registrations = data.get("registered_usernames", [])
        except KeyError as error:
            raise ValidationError(
                f"Dữ liệu sự kiện thiếu trường '{error.args[0]}'."
            ) from error
        if not isinstance(raw_registrations, list):
            raise ValidationError("Danh sách đăng ký phải là một danh sách JSON.")
        registrations = [
            validate_username(username) for username in raw_registrations
        ]
        if len(set(registrations)) != len(registrations):
            raise ValidationError("Danh sách đăng ký chứa username trùng lặp.")
        if len(registrations) > event.capacity:
            raise ValidationError("Số đăng ký trong dữ liệu vượt quá sức chứa.")
        event.registered_usernames = registrations
        return event
