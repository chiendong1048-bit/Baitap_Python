x = 5 #int (có thể là số dương hoặc là số âm ví dụ: -999999, 5555555)
y = 1.5 #float (số thập phân có thể là âm hoặc dương ví dụ: -99.99  , 4589534) decimals: số thập phân,  e là 10^x ví dụ 35e3 35 x 10^3
#5e-3 ---> 5 x 10^-3
z = 1j # j là phần ảo(imaginary part)
print(type(x))
print(type(y))
print(type(z))
a = float(x) #chuyển từ int sang float
print(a)
b = int(y)
print(b) #chuyển từ float sang int
c = complex(x)
print(c) #chuyển từ int sang complex
print(type(a))
print(type(b))
print(type(c))
#không thể chuyển từ complex sang int hay float 
import random
print(random.randrange(1, 10))
# đổi từ float,str sang int
x = int(2)
print(x)
y = int(-99.456)
print(y)
z = int("3")
print(z)
# đổi từ str,int sang float
x = float(1)
y = float(2.8)
z = float("3")
print(x)
print(y)
print(z)
# chuyển từ float,int sang str
x = str("s1")
y = str('2')
z = str("3.0")
print(x)
print(y)
print(z)
print("Tôi tên là 'Chiến'")
print('Tôi tên là "Chiến"')
a = "Hello"
print(a)
b ='''Tôi tên là Đồng Tố Chiến, 
tôi năm nay 20 tuổi, 
tôi thích ăn cơm với chuối đậu.'''
print(b)
a = "Chien"
print(a[1])
for x in "banana": #for dùng để lặp các chữ trong python
    print(x)
b = "Hello, World"   
print(len(b)) #bắt đầu đếm từ số 1 là chữ H
# in được sử dụng để check 1 cụm từ có tồn tại trong chuỗi hay không 
text = "Tôi là một quant trader"
print("trader" in text) #nếu có trong text sẽ hiện ra là true
print("hello" in text)# nếu không có trong text sẽ hiện ra là false
if "trader" in text:
    print("Yes, 'trader' is present")
print("hello" not in text) # sẽ cho kết quả là true vì ko có trong text
if "hello" not in text:
    print("No,'hello' is not present ")
text = "Hello world!"
x = print(text[1])
print(text[2:5]) # đếm từ số 0 còn len thì đếm từ số 1
print(text[:5]) #đếm từ vị trí số 0 đến 5
print(text[2:]) #đếm từ vị trí số 2 đến hết
print(b[-5:-2]) #! là -1 đến d là -2
#-5 là bắt đầu còn -2 là kết thúc nhưng ko lấy vị trí -2
# upper() trả về chuỗi giá trị là chữ in hoa
a = "chien"
print(a.upper()) #trả về là CHIEN
#lower() trả về chuỗi giá trị là chữ thường
b = "CHIEN"
print(b.lower()) #trả về là chien
#strip() loại bỏ khoảng trắng 
a = " Hello, World " 
print(a.strip()) 
# replace() thay thế 1 chuỗi giá trị 
print(a.replace("Hello", "Betto"))
#split() chia 1 chuỗi giá trị thành từng chuỗi nhỏ
print(a.split(","))
#Nối chuỗi- string concatenation
a = "Hello"
b = "World"
c = a + ' ' + b
print(c)
# f-strings dùng để kết nối string và số với nhau
tuổi = 20
tên = "Đồng Tố Chiến"
print(f"Tên tôi là {tên}, Năm nay tôi {tuổi} tuổi")
gia_xang = 50 
print(f"Giá xăng hiện tại là: {gia_xang:.2f} dollars")
print(f"Giá xăng hiện tại là: {gia_xang * 20} dollars")
# \" chèn thêm kí tự mình muốn chèn thêm
print("Tôi tên là \"Chien\" tôi đến từ lớp A15")
print('It\'s right ') #nó sẽ in ra là it's right
print("Điều này rất quan trọng\\(Hãy nhớ kĩ)") #Nó sẽ in ra là Điều này rất quan trọng\(Hãy nhớ kĩ)
print("Tôi tên là\nChien") #nó sẽ in ra chữ Chien ở 1 dòng mới
print("Tôi là siêu\rnhân") #\r đưa con trỏ chuột về đầu dòng
print("Hello cả \tnhà") # dùng khi căn chỉnh hàng mà ko cần gõ phím nhiều lần
print("quant \btrader") # xóa đi khoảng trắng
# capitalize():viết hoa chữ cái đầu tiên
a = "chiến thích ăn chuối đậu"
print(a.capitalize())
#title():viết hoa đầu mỗi từ
b = "Chiến muốn làm quant trader"
print(b.title())
#Bài tập 
#Bài tập 1
ticker = "      aapl     "
print(ticker.upper().strip())
#Bài tập 2
news = "Gold prices are surging today!"
print(news.endswith("!")) #hỏi xem có xuất hiện ở cuối ko
print(news.find("prices")) # tìm vị trí từ prices
print(news.replace("surging","falling")) # thay thế chữ surging thành falling
#Bài tập 3
raw_data = "BTC;64000;2024-04-08"
data_list = raw_data.split(";")
print(data_list)
print(data_list[0])
#Bài tập 4
price_1 = "150"
price_2 = "150.5"
print(price_1.isdigit()) #kiểm tra giá trị có phải toàn số hay ko
print(price_2.isdigit())
#Bài tập tổng hợp
input_str = "    msft:400   "
c = input_str.strip().upper().split(":")
c[1] = int(c[1])
print(c)
"""
1. Nhóm Thay đổi hình thức (Hay dùng để chuẩn hóa dữ liệu)
upper() / lower(): Biến tất cả thành chữ HOA / chữ thường. (Cực kỳ quan trọng để so sánh dữ liệu).

strip(): Cắt bỏ khoảng trắng dư thừa ở hai đầu. (Dùng để dọn dẹp dữ liệu rác).

capitalize() / title(): Viết hoa chữ cái đầu tiên / Viết hoa đầu mỗi từ.

2. Nhóm Tìm kiếm & Kiểm tra (Dân Quant cực kỳ cần)
find(x): Tìm vị trí của x trong chuỗi. Nếu không thấy trả về -1.

count(x): Đếm xem x xuất hiện bao nhiêu lần.

startswith(x) / endswith(x): Kiểm tra chuỗi có bắt đầu hoặc kết thúc bằng x không (Trả về True/False).

replace(cũ, mới): Thay thế chữ cũ bằng chữ mới.

3. Nhóm Tách & Gộp (Dùng để xử lý file dữ liệu CSV/Excel)
split(x): Cắt một chuỗi thành một List dựa trên ký tự x. (Ví dụ: tách họ và tên).

join(): Gộp các phần tử trong List thành một chuỗi.

splitlines(): Tách chuỗi theo từng dòng (dùng khi đọc file văn bản dài).

4. Nhóm Kiểm tra tính chất (Dòng is...)
isdigit(): Có phải toàn là số không? (Dùng để kiểm tra dữ liệu giá trước khi ép kiểu int()).

isalpha(): Có phải toàn là chữ cái không?

isalnum(): Có phải là chữ hoặc số (không chứa ký tự đặc biệt) không?
"""


