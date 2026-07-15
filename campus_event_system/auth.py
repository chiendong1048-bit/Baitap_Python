"""Registration, lookup, and login services."""

from exceptions import AuthenticationError, UserNotFoundError, ValidationError
from models import (
    Admin,
    Organizer,
    StudentVisitor,
    clean_whitespace,
    user_from_dict,
    validate_username,
)
from security import hash_password, verify_password
import storage


ROLE_MENU = {
    "1": Admin,
    "2": Organizer,
    "3": StudentVisitor,
}


class AuthManager:
    def __init__(self):
        self.users = {}
        self._next_id = 1
        self._load()

    def _load(self):
        raw_users = storage.load_users()
        seen_ids = set()
        for item in raw_users:
            user = user_from_dict(item)
            if user.username in self.users:
                raise RuntimeError(
                    f"Dữ liệu chứa username trùng lặp: '{user.username}'."
                )
            if user.user_id in seen_ids:
                raise RuntimeError(f"Dữ liệu chứa User ID trùng lặp: {user.user_id}.")
            self.users[user.username] = user
            seen_ids.add(user.user_id)
        if seen_ids:
            self._next_id = max(seen_ids) + 1

    def save(self):
        users = sorted(self.users.values(), key=lambda user: user.user_id)
        storage.save_users([user.to_dict() for user in users])

    def register(self, username, password, full_name, role_key):
        cleaned_username = validate_username(username)
        if cleaned_username in self.users:
            raise ValidationError(
                f"Tài khoản '{cleaned_username}' đã tồn tại trong hệ thống."
            )
        role_class = ROLE_MENU.get(str(role_key))
        if role_class is None:
            raise ValidationError("Lựa chọn vai trò không hợp lệ.")
        if not password or not str(password).strip():
            raise ValidationError("Mật khẩu không được để trống.")

        user = role_class(
            self._next_id,
            cleaned_username,
            hash_password(str(password)),
            full_name,
        )
        self.users[user.username] = user
        self._next_id += 1
        self.save()
        return user

    def login(self, username, password):
        cleaned_username = clean_whitespace(username)
        user = self.users.get(cleaned_username)
        if user is None:
            raise AuthenticationError("Tài khoản không tồn tại.")
        if not verify_password(str(password), user.password_hash):
            raise AuthenticationError("Mật khẩu không đúng.")
        return user

    def get_user(self, username):
        cleaned_username = clean_whitespace(username)
        user = self.users.get(cleaned_username)
        if user is None:
            raise UserNotFoundError(
                f"Không tìm thấy tài khoản '{cleaned_username}'."
            )
        return user

    def has_user(self, username):
        return clean_whitespace(username) in self.users
