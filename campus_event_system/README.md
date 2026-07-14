# Campus Event Management System

Ứng dụng console Python đáp ứng **Assignment Option 1**: quản lý sự kiện
trong trường với phân quyền Admin, Event Organizer và Student/Visitor.

## Chạy chương trình

```bash
cd campus_event_system
python3 main.py
```

Lần chạy đầu tiên tạo tài khoản minh họa:

- Username: `admin`
- Password: `admin123`

Đây chỉ là tài khoản phục vụ bài tập. Không dùng thông tin mặc định này cho
hệ thống thật.

## Chạy kiểm thử

```bash
python3 -m unittest -v test_system.py
flake8 --max-line-length=88 \
  auth.py exceptions.py main.py managers.py models.py storage.py test_system.py
```

Bộ kiểm thử gồm **63 test cases**, bao phủ:

- Chuẩn hóa và kiểm tra username, họ tên, tên sự kiện, ngày, sức chứa, mô tả.
- Đăng ký, đăng nhập và dữ liệu role không hợp lệ.
- Phân quyền CRUD sự kiện.
- Student/Visitor tự đăng ký và hủy đăng ký.
- Organizer thêm/hủy đăng ký cho sự kiện mình phụ trách.
- Chặn đăng ký trùng, sự kiện đầy, người dùng không tồn tại và sai role.
- Tìm kiếm theo tên/mô tả/ngày, lọc sự kiện còn chỗ.
- Tổng lượt tham gia, sự kiện đông/ít nhất, kể cả trường hợp đồng hạng.
- JSON persistence, dữ liệu hỏng, CSV UTF-8 cho tiếng Việt.

## Cấu trúc

| File | Trách nhiệm |
|---|---|
| `models.py` | `User`, các role, `Event`, chuẩn hóa và validation |
| `auth.py` | Đăng ký, đăng nhập, tra cứu tài khoản |
| `managers.py` | CRUD, phân quyền, đăng ký, tìm kiếm, thống kê |
| `storage.py` | JSON persistence và CSV export |
| `exceptions.py` | Hệ thống custom exceptions |
| `main.py` | Giao diện console tiếng Việt |
| `test_system.py` | 63 test cases tự động |

## Dữ liệu sinh ra

- `data/users.json`
- `data/events.json`
- `reports/event_report_*.csv`

Hai thư mục này được tạo tự động và không cần tạo trước.
