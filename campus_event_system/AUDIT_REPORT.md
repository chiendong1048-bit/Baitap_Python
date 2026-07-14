# Báo cáo đối chiếu Assignment Option 1

## Kết luận

Bản `campus_event_system.pdf` có nhiều cải tiến về validation và giao diện,
nhưng **chưa đủ điều kiện nộp nguyên trạng**. PDF là bản in 34 trang của mã
nguồn, thiếu flowchart và ảnh tương tác; đồng thời có lỗi runtime và thiếu
quyền quan trọng của Event Organizer.

Bản trong thư mục này đã đưa mã về đúng định dạng `.py`, sửa các lỗi và bổ
sung tài liệu/test.

## Các vấn đề phát hiện trong PDF

1. `student_menu` in kết quả bằng biến `event_id` chưa được khai báo thay vì
   `e.event_id`, gây `NameError` khi tìm kiếm có kết quả.
2. Event Organizer chỉ xem danh sách đăng ký, không thể thêm/hủy đăng ký,
   trái yêu cầu “Manage attendee registration for their events”.
3. `update_event` gọi `int(...)` trước validation; dữ liệu như `abc` tạo
   `ValueError` ngoài nhóm `CampusEventError` và có thể đóng ứng dụng.
4. `user_from_dict` biến mọi role không nhận biết thành `StudentVisitor`,
   che giấu dữ liệu bị hỏng.
5. Việc organizer có tồn tại và đúng role chỉ được kiểm tra trong UI, có thể
   bị bỏ qua khi gọi manager trực tiếp.
6. Validation mô tả quá hạn chế, từ chối nhiều dấu câu hợp lệ như `:`, `/`,
   `(`, `)`, `'`, `+`.
7. Chỉ có 9 test methods trong PDF; chưa bao phủ CRUD, phân quyền Organizer,
   persistence, CSV, search runtime, thống kê, dữ liệu hỏng và update atomic.
8. Thiếu flowchart, ảnh minh họa từng role và phần mô tả class/method theo
   Submission Requirements.

## Đối chiếu yêu cầu sau sửa

| Yêu cầu | Trạng thái |
|---|---|
| Admin tạo/cập nhật/xóa sự kiện | Đạt |
| Admin xem sự kiện và người tham gia | Đạt |
| Organizer quản lý đăng ký sự kiện của mình | Đạt |
| Organizer xem chi tiết sự kiện | Đạt |
| Student/Visitor tìm kiếm, đăng ký, xem sự kiện đã đăng ký | Đạt |
| Validation tên, ngày, sức chứa | Đạt |
| Capacity check, duplicate prevention, confirmation | Đạt |
| Tổng lượt tham gia, đông nhất, ít nhất | Đạt, hỗ trợ đồng hạng |
| JSON persistence | Đạt |
| CSV report | Đạt, UTF-8 BOM cho Excel |
| OOP và modular design | Đạt |
| Flowchart | Có trong tài liệu bàn giao |
| Screenshots cho ba role | Có trong tài liệu bàn giao |

## Kết quả kiểm thử

- File `.py` cũ đính kèm: **34/34** scenario checks pass, nhưng coverage chưa
  phát hiện các thiếu sót của PDF.
- Bản hoàn chỉnh: **63/63** unit/integration tests pass.
- CLI end-to-end: đăng ký tài khoản, Admin tạo sự kiện, Organizer thêm người
  tham gia, Student tìm kiếm/xem/hủy đăng ký, Admin xem thống kê và xuất CSV
  đều chạy thành công.
- `py_compile`: pass.
- `flake8 --max-line-length=88`: pass.
