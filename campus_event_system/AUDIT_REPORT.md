# Final Audit Report — Campus Event Management System

Nguồn đối chiếu: `Assignment - Option 1 - Subject.docx` và bộ
`campus_event_system_optimized.zip`.

## Kết luận

Source tối ưu ban đầu đã triển khai đủ chức năng chính và pass 76 tests. Tuy
nhiên, **submission package chưa đồng bộ hoàn toàn**:

1. `documentation/test_case_matrix.csv` và `test_results.txt` vẫn chỉ có 63
   tests.
2. PDF/DOCX report vẫn ghi 63/63 và còn nói password plaintext.
3. Flowchart/report cũ chưa thể hiện PBKDF2, reminder hoặc hạn chế public
   Admin signup.
4. README table ghi nhóm search/persistence là 14 nhưng thực tế có 15 tests.
5. Một số data-integrity và boundary cases chưa được test.

Các điểm trên đã được sửa. Bản cuối có:

- 93/93 automated tests PASS.
- 24 acceptance test cases.
- 17 runtime assertions PASS.
- `py_compile`/`flake8` PASS.
- 90% branch-inclusive source coverage với unit + CLI E2E.
- Flowchart, class diagram, role screenshots, PDF/DOCX report và matrices mới.

## Requirement matrix

| Assignment requirement | Status | Evidence |
|---|---|---|
| Admin create/update/delete events | PASS | `EventManager`, Admin CLI |
| Admin view all events/attendees | PASS | Admin menu and E2E |
| Organizer manage own registrations | PASS | Ownership enforcement |
| Organizer view event details | PASS | Own-event listing + attendees |
| Student/Visitor search/register/view | PASS | Search filters and self-only RBAC |
| Validate event name/date/capacity | PASS | Domain validation + boundaries |
| Capacity check and confirmation | PASS | `EventFullError`, success messages |
| Prevent duplicate registration | PASS | `DuplicateRegistrationError` |
| Total/highest/lowest attendance | PASS | Empty and tie cases covered |
| Persist event/attendee data | PASS | JSON atomic replacement |
| Export statistical report | PASS | UTF-8 BOM CSV |
| OOP and modular code | PASS | Abstract User hierarchy/managers |
| Flowchart | PASS | PNG + editable Mermaid |
| Class/method description | PASS | README, report, class diagram |
| Role screenshots | PASS | Admin/Organizer/Student PNG files |
| Creativity | PASS | Multi-filter search + 7-day reminders |

## Code improvements added in this audit

1. Username validation được dùng thống nhất khi đăng ký và khi load JSON.
2. User ID/Event ID từ chối `bool` và số thập phân thay vì âm thầm ép kiểu.
3. Persisted user/event entries phải là JSON object.
4. Persisted registration phải là list username hợp lệ.
5. Event load kiểm tra Organizer/attendee tồn tại và đúng role.
6. Reminder window/date input được validate.
7. Startup bắt domain corruption và in lỗi hệ thống, không traceback.
8. Public signup không cho tạo Admin.
9. Password prompt giữ nguyên whitespace có ý nghĩa.
10. Admin có thể nhập `-` để xóa description optional.
11. Test suite khôi phục PBKDF2 iteration count sau khi chạy.
12. Bổ sung test duplicate persisted IDs và CSV path traversal.

## Test result

```text
Ran 93 tests
OK
```

```text
python3 -m py_compile ...  PASS
flake8 ...                 PASS
CLI exit status            0
Runtime assertions         17/17 PASS
Branch-inclusive coverage  90%
```

Chi tiết nằm trong `documentation/`.

## Submission checklist

- [x] Runnable Python source
- [x] README và hướng dẫn chạy
- [x] Flowchart PNG + Mermaid source
- [x] Class diagram PNG + Mermaid source
- [x] 93-case automated test matrix
- [x] 24-case manual acceptance matrix
- [x] Requirement traceability matrix
- [x] Test output and coverage
- [x] Admin screenshot
- [x] Event Organizer screenshot
- [x] Student/Visitor screenshot
- [x] Runtime CLI transcript
- [x] Runtime JSON/CSV evidence
- [x] Submission report PDF
- [x] Submission report DOCX
