# noi ra noi dung minh lam trong task nay 
"""
    Bạn có thể viết nhiều nội dung trong này và python sẽ phớt lờ nó
    Học python với chiến béo
    Học python để làm data science
    """
# để viết cùng dòng có thể sử dụng lệnh sau
print("Tôi là học sinh lớp 1",  end="năm nay tôi 18 tuổi")
# cách khai báo biến của python
x = 5
y ="Hello,World"
# bạn có thể code nhiều dòng lệnh trên 1 dòng ví dụ:
print("Hello world");print("Tôi muốn ăn cơm.");print("Tôi muốn uống nước.")
#In ra các con số
print(3)
print(358)
#In ra các phép tính toán
print(3+3)
print(2 * 5)
 #In ra cả chữ lẫn số trên cùng 1 dòng
print("Tôi tên là Chiến");print("Năm nay tôi:", 20,"tuổi")     
#Khai báo biến trong python(không có lệnh khai báo biến)
"""
5 là int
John là str
19.5 là float

"""
x = 5
y = "John"
print(x)
print(y)
#Cách chuyển từ int sang str, từ int sang float
x = str(3)
z = float(3)
print(x)
print(y)
#nếu code x=3 và x="Hello" thì nó sẽ in ra giá trị gần nhất
x = 3
x = "hello"
print(x)
#gọi ra kiểu ví dụ như là int,str,float
x = 19.5
y = "Hello bố mày là nhất"
print(type(y))
print(type(x))
#Việc dùng "" hay '' đều giống nhau 
# các dấu trong tiếng anh và cách đọc
"""
double quotes:""
single quote:''
parenthese hoặc round brackets:()
curly brackets/braces:{}
square brackets: []
angle brackets: <>
"""
#trường hợp đặc biệt giữa chữ thường và chữ hoa trong python
a = 4
A = "sally"
print(a)
print(A)
#Tên biến: một biến có thể là x hoặc y hoặc mang tính miêu tả ví dụ (tuổi,tên,...)
"""
Tên biến cần bắt đầu với một chữ cái hoặc một dấu gạch dưới(underscore character)
ví dụ: ten = "chien"
       ho_ten = "dong chien"
       _ho_ten = "dong chien" 
Tên biến chỉ có thể chứa các giá trị số và chữ từ (A đến z và từ 0 đến 9)
Phân biệt biến ví dụ age,Age,AGE là 3 biến khác nhau
Tên biến ko thể dùng các lệnh của python
MYNAME = "John"
myname2 = "Chien"
Kieu bien Camel Case: mỗi từ trừ từ ngữ đầu tiên đều viết hoa
ví dụ: myNameIS = "Chien"
kiểu biến Pascal case: mỗi từ đều bắt đầu bằng một chữ hoa:
ví dụ: MyNameIs = "Chien"
kiểu biến Snake case: mỗi từ được tách bằng dấu gạch dưới
ví dụ: my_name_is = "Chien"
"""
# Biến trong Python - Nhập nhiều giá trị
x,y,z = "Cam" , "Ổi" , "Táo"
print(x)
print(y)
print(z)
# Một giá trị nhưng nhiều biến 
x = y = z = "Lan"
print(x)
print(y)
print(z)
#Unpacking trong Python
fruits = ["apple", "banana", "cherry"]
x,y,z = fruits
print(x)
print(y)
print(z)
#Biến đầu ra
x = "Chien is a good boy"
print(x)

x = "Python"
y = "is"
z = "awesome"
print(x,y,z)
print(x  +  y  +  z)
x = 5
y = 10
print(x+y)
x = 5
y = "John"
print(x,y)
#Global variables :biến toàn cục
x = "Chienbeo"
def myfunc():
    print("Phuong Anh yeu" + x )
myfunc()
x = "awesome"
def myfunc():
    x = "fantastic"
    print("Python is " + x )
myfunc()
print("Python is " + x)
# nếu ở trong thì sẽ ra giá trị là Python is fantastic còn ở ngoài thì ra giá trị là Python is awesome
# nếu muốn sử dụng biến ở trong 1 hàm thì cần sử dụng global
def concho():
    global x 
    x = "dumaSaiGon"
concho()
print("Sai Gon dep lam Sai Gon oi Sai Gon oi" + x )
#Để thay đổi một biến global trong 1 hàm kham khảo cách sử dụng biến sau
x = "awesome"
def dumamay():
    global x
    x = "mày có đẹp trai đéo đâu"
dumamay()
print("Tao nói thế mà mày cũng tin à!" + x )

    

    



