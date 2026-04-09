#Boolean đại diện cho 2 giá trị True và False
print(10 > 9)
print(5 == 3)
print(9 < 8)
"""
>,<,==(bằng),!=(khác,không bằng),>=(lớn hơn hoặc bằng),=<
"""
a = 500
b = 100
if b > a:
 print("b is greater than a")
else:
 print("b is not greater than a")
 print(bool("Hello"))
 print(bool(15))

x = 5
y = "Tôi tên là Chiến"
print(bool(x))
print(bool(y))
# str almost true expect empty str
# number alsmot true expect 0
# bất kì list[], tuple(), set{}, dictionary{} đều true trừ những cái nào chống
bool("abc")
bool(15)
bool(["banana", "apple", "strawberry"])
#Các giá trị sau sẽ bị đánh giá là sai
print(bool(False))
print(bool(None))
print(bool(""))
print(bool(()))
print(bool([]))
print(bool({}))
print(bool(0))
class MyWallet:
    def __len__(self):
        return 10  # Giả sử trong ví có 10 đô

wallet = MyWallet()
print(bool(wallet))

class Botsanmoi: #bản thiết kế muốn ai đó làm gì
   #def(là define-định nghĩa) tạo hành động để bot thực hiện
   def dat_lenh_mua():
      #len là length(độ dài)-là một thước đo mặc định của python
      #len(list_co_phieu): chỉ đo được danh sách hoặc chuỗi bình thường
      #def _ _ len _ _(self): thước đo của python giúp bạn đo
      #self (chính tôi):đo đạc dữ liệu của chính nó ko (python) ko phải ngôn ngữ khác

# 1. Tạo bản thiết kế (class)
    class DanhMucCuaToi:
     def __init__(self):
        self.danh_sach_co_phieu = ["AAPL", "TSLA"] # Dữ liệu bên trong máy

    # 2. Dạy máy cách trả lời khi bị đo độ dài (def __len__)
     def __len__(self):
        # Khi ai đó dùng len() với cái máy này, nó sẽ trả về số lượng cổ phiếu
        return len(self.danh_sach_co_phieu)

# 3. Xuất xưởng cái máy thực tế (Object)
    my_portfolio = DanhMucCuaToi()

# 4. Sử dụng cái thước đo (len)
    print(len(my_portfolio)) 
# Kết quả sẽ ra là 2.
#print câu trả lời về hàm
def myfunction() :
  return True
print(myfunction())

def myfunction() :
  return True
if myfunction():
  print("Yes!")
else:
  print("No!")
  #cấu trúc của isinstance(đối tượng, kiểu dữ liệu):
  x = 200
  print(isinstance(x,int))
  



