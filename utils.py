"""Các hàm tiện ích dùng chung cho các bài tập Python.

Gom những đoạn code bị lặp lại ở nhiều file (tính toán số học, hình học,
đa thức, trung bình...) vào một chỗ để tái sử dụng.
"""


# --- Nhóm phép toán số học cơ bản ---
def tong(a, b):
    """Trả về tổng của a và b."""
    return a + b


def hieu(a, b):
    """Trả về hiệu của a và b."""
    return a - b


def tich(a, b):
    """Trả về tích của a và b."""
    return a * b


def thuong(a, b):
    """Trả về thương của a chia b."""
    return a / b


def chia_lay_du(a, b):
    """Trả về phần dư của a chia b."""
    return a % b


def luy_thua(a, b):
    """Trả về a mũ b."""
    return a ** b


# --- Nhóm hình học ---
def dien_tich_hcn(chieu_dai, chieu_rong):
    """Diện tích hình chữ nhật."""
    return chieu_dai * chieu_rong


def chu_vi_hcn(chieu_dai, chieu_rong):
    """Chu vi hình chữ nhật."""
    return (chieu_dai + chieu_rong) * 2


# --- Nhóm đa thức & thống kê ---
def gia_tri_bac_hai(a, b, c, x):
    """Tính giá trị đa thức bậc hai a*x^2 + b*x + c tại x."""
    return (a * x ** 2) + (b * x) + c


def trung_binh(*so):
    """Trả về giá trị trung bình cộng của các số truyền vào."""
    return sum(so) / len(so)


# --- Nhóm xử lý chuỗi ---
def chuan_hoa_chuoi(chuoi):
    """Chuẩn hóa chuỗi: bỏ khoảng trắng thừa và viết hoa toàn bộ."""
    return chuoi.strip().upper()
