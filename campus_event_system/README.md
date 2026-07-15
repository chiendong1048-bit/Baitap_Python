# Campus Event Management System

Ứng dụng console Python hoàn chỉnh cho **Assignment Option 1 — Building a
Campus Event Management System with Role-Based Access**.

## Kết quả kiểm tra cuối

- **93/93 automated tests PASS**.
- **24 manual acceptance scenarios** được lập tài liệu.
- `py_compile` và `flake8` PASS.
- CLI end-to-end Admin → Organizer → Student/Visitor → Admin thoát với code `0`.
- **17 runtime assertions PASS**, không có traceback.
- Startup với JSON sai cấu trúc hiển thị lỗi thân thiện và dừng an toàn.
- **90% branch-inclusive source coverage** khi kết hợp unit tests và CLI E2E.

Xem toàn bộ bằng chứng trong [`documentation/`](documentation/):

- `flowchart.png` / `flowchart.mmd`
- `class_diagram.png` / `class_diagram.mmd`
- `test_case_matrix.csv` — 93 automated cases
- `manual_acceptance_test_cases.csv` — 24 acceptance cases
- `requirements_traceability.csv`
- `campus_event_system_submission_report.pdf` / `.docx`
- role screenshots, test output, coverage và CLI transcript

## Chạy chương trình

```bash
cd campus_event_system
python3 main.py
```

Tài khoản Admin demo được tạo khi dữ liệu chưa có user:

```text
Username: admin
Password: admin123
```

Đây là tài khoản minh họa cho bài tập, không dùng trong production.

## Chạy kiểm thử và quality checks

```bash
python3 -m unittest -v test_system.py

python3 -m py_compile \
  auth.py exceptions.py main.py managers.py models.py security.py storage.py \
  test_system.py

flake8 --max-line-length=88 \
  auth.py exceptions.py main.py managers.py models.py security.py storage.py \
  test_system.py
```

Phân bố 93 tests:

| Nhóm | Cases |
|---|---:|
| Input validation | 17 |
| Authentication & persisted users | 10 |
| Password security & public signup | 10 |
| RBAC & event CRUD | 13 |
| Attendee registration | 14 |
| Search, reports & persistence | 22 |
| Automated reminders | 7 |
| **Tổng** | **93** |

## Chức năng theo vai trò

### Admin

- Xem tất cả sự kiện và danh sách người tham gia.
- Tạo, cập nhật và xóa sự kiện.
- Validate tên, ngày, capacity và Event Organizer.
- Không cho giảm capacity thấp hơn số registration hiện tại.
- Xem tổng lượt đăng ký, event đông/ít nhất và trường hợp đồng hạng.
- Xuất báo cáo CSV.

### Event Organizer

- Xem chi tiết các event mình phụ trách.
- Xem attendee của event.
- Thêm/hủy registration cho Student/Visitor.
- Không thể quản lý event của Organizer khác.
- Nhận reminder cho event mình phụ trách trong 7 ngày tới.

### Student/Visitor

- Tìm theo tên, mô tả và ngày.
- Lọc chỉ event còn chỗ.
- Tự đăng ký/hủy đăng ký; không thể thao tác cho user khác.
- Xem event đã đăng ký.
- Nhận reminder cho event đã đăng ký trong 7 ngày tới.

## Business rules và validation

- Username phải là chuỗi chữ/số, tối đa 30 ký tự.
- Họ tên hỗ trợ tiếng Việt, dấu nháy và dấu gạch nối.
- Ngày bắt buộc `YYYY-MM-DD` và phải tồn tại trên lịch.
- Capacity là số nguyên từ `1` đến `100,000`.
- Event ID/User ID phải là số nguyên dương; từ chối `bool` và số thập phân.
- Chặn registration trùng và event hết chỗ.
- Organizer/attendee trong JSON phải tồn tại và đúng role.
- Update event được dựng trên object mới trước khi thay thế nên không để lại
  trạng thái cập nhật dở nếu validation thất bại.
- JSON root, object, duplicate ID, duplicate registration và cross-file
  references đều được kiểm tra khi load.

## Bảo mật

`security.py` dùng PBKDF2-HMAC-SHA256, salt ngẫu nhiên 16 byte và
`hmac.compare_digest`. `users.json` chỉ lưu `password_hash`, không lưu mật
khẩu gốc.

Public signup chỉ cho phép:

- Event Organizer
- Student/Visitor

Admin không xuất hiện trong public signup; tài khoản Admin demo được seed từ
code cho phạm vi assignment.

## OOP và module structure

| File | Trách nhiệm |
|---|---|
| `models.py` | Validation, `User` abstract class, role subclasses, `Event` |
| `auth.py` | Registration, login, user lookup và persistence |
| `security.py` | Password hashing và verification |
| `managers.py` | CRUD, RBAC, registration, search, statistics, reminder |
| `storage.py` | JSON atomic replacement và UTF-8 CSV export |
| `exceptions.py` | Custom exception hierarchy |
| `main.py` | Vietnamese console UI và role routing |
| `test_system.py` | 93 automated requirement/boundary/security tests |
| `documentation/` | Flowchart, class diagram, test cases, screenshots, report |

`User` là abstract base class. `Admin`, `Organizer` và `StudentVisitor` kế
thừa và override `role_name()`/`menu_options()`, thể hiện inheritance và
polymorphism. Business rules nằm trong `EventManager`, không phụ thuộc vào UI.

## Data files

Chương trình tự tạo:

```text
data/users.json
data/events.json
reports/event_report_YYYYMMDD_HHMMSS_microseconds.csv
```

JSON được ghi qua temporary file rồi `os.replace`. CSV dùng UTF-8 BOM để mở
đúng tiếng Việt trong Excel và gồm:

```text
event_id, name, date, organizer, capacity, registered,
seats_left, status, attendees
```

## Giới hạn ngoài phạm vi assignment

- JSON phù hợp bài tập/single-process, không thay thế database cho hệ thống
  nhiều người dùng đồng thời.
- Chưa có rate limiting, reset password hoặc MFA.
- Demo Admin có credential cố định để giảng viên chạy bài nhanh.
- Reminder là thông báo khi login, không gửi email/SMS background.
