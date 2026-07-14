"""JSON persistence and CSV report export."""

import csv
import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
EVENTS_FILE = os.path.join(DATA_DIR, "events.json")


def _ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)


def load_json(path):
    """Load a JSON list, returning an empty list when the file is absent."""
    _ensure_dirs()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read().strip()
        if not content:
            return []
        data = json.loads(content)
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"Tệp dữ liệu '{path}' bị hỏng hoặc sai cấu trúc JSON: {error}."
        ) from error
    except OSError as error:
        raise RuntimeError(f"Không thể đọc tệp '{path}': {error}.") from error
    if not isinstance(data, list):
        raise RuntimeError(f"Tệp dữ liệu '{path}' phải chứa một danh sách JSON.")
    return data


def save_json(path, data):
    """Write JSON through a temporary file before replacing the target."""
    _ensure_dirs()
    temporary_path = path + ".tmp"
    try:
        with open(temporary_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temporary_path, path)
    except OSError as error:
        try:
            if os.path.exists(temporary_path):
                os.remove(temporary_path)
        except OSError:
            pass
        raise RuntimeError(f"Không thể lưu dữ liệu vào '{path}': {error}.") from error


def load_users():
    return load_json(USERS_FILE)


def save_users(users_data):
    save_json(USERS_FILE, users_data)


def load_events():
    return load_json(EVENTS_FILE)


def save_events(events_data):
    save_json(EVENTS_FILE, events_data)


def export_csv(filename, headers, rows):
    """Export rows using UTF-8 BOM so Vietnamese text opens correctly in Excel."""
    _ensure_dirs()
    safe_filename = os.path.basename(filename)
    if safe_filename != filename or not safe_filename.lower().endswith(".csv"):
        raise ValueError("Tên báo cáo phải là tên tệp CSV hợp lệ.")
    path = os.path.join(REPORTS_DIR, safe_filename)
    try:
        with open(path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
    except OSError as error:
        raise RuntimeError(f"Không thể xuất báo cáo '{path}': {error}.") from error
    return path
