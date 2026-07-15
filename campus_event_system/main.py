"""Vietnamese console interface for the campus event system."""

from auth import AuthManager
from exceptions import CampusEventError
from managers import EventManager
from models import Admin, Organizer, StudentVisitor, clean_whitespace


def prompt(label):
    return input(label)


def prompt_nonempty(label):
    while True:
        value = clean_whitespace(prompt(label))
        if value:
            return value
        print("  [Lỗi] Nội dung không được để trống.")


def prompt_password(label):
    while True:
        value = prompt(label)
        if value and value.strip():
            return value
        print("  [Lỗi] Mật khẩu không được để trống.")


def prompt_choice(label, valid_choices):
    while True:
        value = prompt(label).strip()
        if value in valid_choices:
            return value
        print(f"  [Lỗi] Vui lòng chọn một trong: {', '.join(valid_choices)}.")


def prompt_int(label):
    while True:
        value = prompt_nonempty(label)
        try:
            return int(value)
        except ValueError:
            print("  [Lỗi] Vui lòng nhập số nguyên.")


def prompt_optional_int(label, current_value):
    while True:
        value = prompt(label).strip()
        if not value:
            return current_value
        try:
            return int(value)
        except ValueError:
            print("  [Lỗi] Vui lòng nhập số nguyên hoặc để trống.")


def pause():
    prompt("\nNhấn Enter để tiếp tục...")


def print_header(title):
    print("\n" + "=" * 68)
    print(title)
    print("=" * 68)


def print_event(event):
    status = "HẾT CHỖ" if event.is_full else f"còn {event.seats_left} chỗ"
    print(
        f"[{event.event_id}] {event.name} | {event.date_str} | "
        f"{event.registered_count}/{event.capacity} ({status}) | "
        f"Organizer: {event.organizer_username}"
    )
    if event.description:
        print(f"    Mô tả: {event.description}")


def print_attendees(event, auth_manager):
    print_header(f"Người tham gia - [{event.event_id}] {event.name}")
    if not event.registered_usernames:
        print("Chưa có người đăng ký.")
        return
    for index, username in enumerate(event.registered_usernames, 1):
        user = auth_manager.get_user(username)
        print(f"{index}. {user.full_name} ({user.username})")


def do_register(auth_manager):
    print_header("ĐĂNG KÝ TÀI KHOẢN")
    username = prompt_nonempty("Username (chỉ chữ và số): ")
    password = prompt_password("Mật khẩu: ")
    full_name = prompt_nonempty("Họ và tên: ")
    print("2. Event Organizer\n3. Student/Visitor")
    print("Tài khoản Admin chỉ được cấp sẵn cho mục đích quản trị.")
    role_key = prompt_choice("Chọn vai trò: ", {"2", "3"})
    user = auth_manager.register(username, password, full_name, role_key)
    print(
        f"[Thành công] Đã tạo tài khoản {user.username} "
        f"với vai trò {user.role_name()}."
    )
    return user


def do_login(auth_manager):
    print_header("ĐĂNG NHẬP")
    username = prompt_nonempty("Username: ")
    password = prompt_password("Mật khẩu: ")
    user = auth_manager.login(username, password)
    print(f"[Thành công] Xin chào {user.full_name}.")
    return user


def show_upcoming_reminders(user, event_manager):
    """Automated reminder: flag events happening within the next 7 days."""
    if isinstance(user, StudentVisitor):
        upcoming = event_manager.upcoming_events_for_attendee(user.username)
        label = "SỰ KIỆN BẠN ĐÃ ĐĂNG KÝ SẮP DIỄN RA (7 NGÀY TỚI)"
    elif isinstance(user, Organizer):
        upcoming = event_manager.upcoming_events_for_organizer(user.username)
        label = "SỰ KIỆN BẠN PHỤ TRÁCH SẮP DIỄN RA (7 NGÀY TỚI)"
    else:
        return
    if not upcoming:
        return
    print_header(label)
    for event in upcoming:
        print_event(event)


def admin_menu(user, event_manager, auth_manager):
    while True:
        print_header(f"ADMIN - {user.full_name}")
        for key, label in user.menu_options():
            print(f"{key}. {label}")
        choice = prompt_choice("Lựa chọn: ", {key for key, _ in user.menu_options()})
        try:
            if choice == "1":
                events = event_manager.list_all_events()
                print_header(f"TẤT CẢ SỰ KIỆN ({len(events)})")
                for event in events:
                    print_event(event)
                if not events:
                    print("Chưa có sự kiện.")
            elif choice == "2":
                name = prompt_nonempty("Tên sự kiện: ")
                date_str = prompt_nonempty("Ngày (YYYY-MM-DD): ")
                capacity = prompt_int("Sức chứa: ")
                organizer = prompt_nonempty("Organizer username: ")
                description = prompt("Mô tả (không bắt buộc): ")
                event = event_manager.create_event(
                    user,
                    name,
                    date_str,
                    capacity,
                    organizer,
                    description,
                )
                print(f"[Thành công] Đã tạo sự kiện ID {event.event_id}.")
            elif choice == "3":
                event = event_manager.get_event(prompt_int("Event ID: "))
                print(
                    "Để trống để giữ nguyên; nhập '-' ở mô tả để xóa nội dung."
                )
                name = prompt(f"Tên [{event.name}]: ").strip() or event.name
                date_str = (
                    prompt(f"Ngày [{event.date_str}]: ").strip() or event.date_str
                )
                capacity = prompt_optional_int(
                    f"Sức chứa [{event.capacity}]: ",
                    event.capacity,
                )
                organizer = (
                    prompt(f"Organizer [{event.organizer_username}]: ").strip()
                    or event.organizer_username
                )
                description_input = prompt(
                    f"Mô tả [{event.description or 'trống'}]: "
                )
                if description_input.strip() == "-":
                    description = ""
                elif not description_input.strip():
                    description = event.description
                else:
                    description = description_input
                event_manager.update_event(
                    user,
                    event.event_id,
                    name=name,
                    date_str=date_str,
                    capacity=capacity,
                    organizer_username=organizer,
                    description=description,
                )
                print("[Thành công] Đã cập nhật sự kiện.")
            elif choice == "4":
                event_id = prompt_int("Event ID: ")
                confirm = prompt_choice("Xác nhận xóa? (Y/N): ", {"Y", "N", "y", "n"})
                if confirm.upper() == "Y":
                    event_manager.delete_event(user, event_id)
                    print("[Thành công] Đã xóa sự kiện.")
                else:
                    print("Đã hủy thao tác.")
            elif choice == "5":
                event = event_manager.get_event(prompt_int("Event ID: "))
                print_attendees(event, auth_manager)
            elif choice == "6":
                stats = event_manager.statistics_report()
                print_header("BÁO CÁO THỐNG KÊ")
                print(f"Tổng sự kiện: {stats['total_events']}")
                print(f"Tổng lượt đăng ký: {stats['total_attendees']}")
                highest = stats["highest_events"]
                lowest = stats["lowest_events"]
                print(
                    "Đông nhất: "
                    + (
                        ", ".join(
                            f"{event.name} ({event.registered_count})"
                            for event in highest
                        )
                        if highest
                        else "N/A"
                    )
                )
                print(
                    "Ít nhất: "
                    + (
                        ", ".join(
                            f"{event.name} ({event.registered_count})"
                            for event in lowest
                        )
                        if lowest
                        else "N/A"
                    )
                )
            elif choice == "7":
                path = event_manager.export_statistics_csv()
                print(f"[Thành công] Báo cáo đã lưu tại: {path}")
            else:
                print("Đã đăng xuất.")
                return
        except CampusEventError as error:
            print(f"[Lỗi] {error}")
        pause()


def organizer_menu(user, event_manager, auth_manager):
    while True:
        print_header(f"EVENT ORGANIZER - {user.full_name}")
        for key, label in user.menu_options():
            print(f"{key}. {label}")
        choice = prompt_choice("Lựa chọn: ", {key for key, _ in user.menu_options()})
        try:
            if choice == "1":
                events = event_manager.list_events_for_organizer(user.username)
                print_header(f"SỰ KIỆN CỦA TÔI ({len(events)})")
                for event in events:
                    print_event(event)
                    print_attendees(event, auth_manager)
                if not events:
                    print("Bạn chưa được giao phụ trách sự kiện nào.")
            elif choice == "2":
                event_id = prompt_int("Event ID: ")
                action = prompt_choice(
                    "1. Thêm đăng ký  2. Hủy đăng ký: ",
                    {"1", "2"},
                )
                attendee_username = prompt_nonempty("Student/Visitor username: ")
                if action == "1":
                    event = event_manager.register_attendee(
                        user,
                        event_id,
                        attendee_username,
                    )
                    print(
                        f"[Thành công] Đã đăng ký {attendee_username} "
                        f"({event.registered_count}/{event.capacity})."
                    )
                else:
                    event_manager.unregister_attendee(
                        user,
                        event_id,
                        attendee_username,
                    )
                    print(f"[Thành công] Đã hủy đăng ký {attendee_username}.")
            else:
                print("Đã đăng xuất.")
                return
        except CampusEventError as error:
            print(f"[Lỗi] {error}")
        pause()


def student_menu(user, event_manager, _auth_manager):
    while True:
        print_header(f"STUDENT/VISITOR - {user.full_name}")
        for key, label in user.menu_options():
            print(f"{key}. {label}")
        choice = prompt_choice("Lựa chọn: ", {key for key, _ in user.menu_options()})
        try:
            if choice == "1":
                keyword = prompt("Từ khóa tên/mô tả (có thể để trống): ")
                date_str = prompt("Ngày YYYY-MM-DD (có thể để trống): ")
                only_available = prompt_choice(
                    "Chỉ hiện sự kiện còn chỗ? (Y/N): ",
                    {"Y", "N", "y", "n"},
                )
                results = event_manager.search_events(
                    keyword,
                    date_str,
                    only_available.upper() == "Y",
                )
                print_header(f"KẾT QUẢ TÌM KIẾM ({len(results)})")
                for event in results:
                    print_event(event)
                if not results:
                    print("Không tìm thấy sự kiện phù hợp.")
            elif choice == "2":
                event = event_manager.register_attendee(
                    user,
                    prompt_int("Event ID: "),
                )
                print(
                    f"[Thành công] Đăng ký '{event.name}' thành công. "
                    f"({event.registered_count}/{event.capacity})"
                )
            elif choice == "3":
                event = event_manager.unregister_attendee(
                    user,
                    prompt_int("Event ID: "),
                )
                print(f"[Thành công] Đã hủy đăng ký '{event.name}'.")
            elif choice == "4":
                events = event_manager.events_for_attendee(user.username)
                print_header(f"SỰ KIỆN ĐÃ ĐĂNG KÝ ({len(events)})")
                for event in events:
                    print_event(event)
                if not events:
                    print("Bạn chưa đăng ký sự kiện nào.")
            else:
                print("Đã đăng xuất.")
                return
        except CampusEventError as error:
            print(f"[Lỗi] {error}")
        pause()


MENU_BY_ROLE = {
    Admin: admin_menu,
    Organizer: organizer_menu,
    StudentVisitor: student_menu,
}


def seed_default_admin(auth_manager):
    if not auth_manager.has_user("admin"):
        auth_manager.register("admin", "admin123", "System Admin", "1")


def main():
    auth_manager = AuthManager()
    seed_default_admin(auth_manager)
    event_manager = EventManager(auth_manager)

    while True:
        print_header("CAMPUS EVENT MANAGEMENT SYSTEM")
        print("1. Đăng nhập\n2. Đăng ký tài khoản\n0. Thoát")
        choice = prompt_choice("Lựa chọn: ", {"1", "2", "0"})
        try:
            if choice == "1":
                user = do_login(auth_manager)
                show_upcoming_reminders(user, event_manager)
                MENU_BY_ROLE[type(user)](user, event_manager, auth_manager)
            elif choice == "2":
                do_register(auth_manager)
            else:
                print("Cảm ơn bạn đã sử dụng hệ thống.")
                return
        except CampusEventError as error:
            print(f"[Lỗi] {error}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nChương trình đã dừng an toàn.")
    except (CampusEventError, OSError, RuntimeError) as error:
        print(f"\n[Lỗi hệ thống] {error}")
