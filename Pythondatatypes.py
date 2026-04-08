# data type : kiểu dữ liệu
ten_sv = "Đồng Tố Chiến"
ma_so_sv = 14
diem_toan = 8.5
diem_ly = 8.9
diem_trung_binh = (diem_toan + diem_ly) / 2
print(f"Sinh viên {ten_sv}","mã số sinh viên là:",{ ma_so_sv}, "có điểm trung bình là:", {diem_trung_binh})
# list[]: danh sách ->cho phép thay đổi giá trị,cho phép các giá trị lặp và danh sách xếp theo thứ tự
# trong list[] thì item đầu tiên là số 0 rồi đến 1,2,3....
# ordered sắp xếp theo thứ tự và thứ tự đó không thể thay đổi nếu add cái mới thì xếp ở cuối danh sách
#changeable chúng ta có thể thay đổi, thêm, loại bỏ kí items trong list đã tạo
#allow duplicates(bản sao trùng lặp) cho phép
#ví dụ:
hellolist = ["kem cá","kẹo kéo", "siêu nhân" ]
print(hellolist)
campinglist = ["lều","bếp lửa", "cần câu", "bếp lửa", "đồ ăn"]
print(campinglist)
#để đếm số phần tử có trong một list ta sử dụng len()
print(len(campinglist))
list1 = ["táo","kem","kẹo","cá"]
list2 = [1,2,3,4,5,6]
list3 = [True,False,False]
list4 = [True,"táo","kem",1,4,5]
print(type(list1))
print(type(list2))
cacconvat = list(("con mèo","con cá","con cún"))
print(cacconvat)
#Tuple(sắp xếp theo thứ tự nhưng ko thể thay đổi có thể lặp lại items đc)
mytuple = ("quả táo","quả táo", "quả cam","quả dứa")
print(mytuple)
print(len(mytuple))
#Set(sắp xếp ko theo thứ tự và không thể thay đổi đc,không được lập chỉ mục,không có iemts lặp)
#Dictionary(sắp xếp theo thứ tự,có thể thay đổi được và không có số lặp)
#Nếu không có dấu , thì tuple 1 items sẽ ko phải là tuple
hellotuple = ("quả táo",)
print(type(hellotuple))
concatuple = ("cá mè")
print(type(concatuple)) # đây sẽ là str
thistuple = tuple(("quả cam","quả táo","quả cam","quả chuối"))
print(thistuple)
#Tuple thường dùng cho tọa độ,bản đồ,ngày sinh những thứ chính xác
#Tuple dùng ngoặc ()
diem_so = [8.5 , 9.0 , 7.5]
diem_so.append(10)
diem_so[0] = 9.5
tong_diem = sum(diem_so)
print(tong_diem)
thong_tin_co_dinh = ("Đồng Tố Chiến" , "14" , "Hà Nội")
print(thong_tin_co_dinh)
#Set (không theo tứ tự,không thể thay đổi,không theo chỉ mục)
# Set dùng ngoặc{}
thisset = {"Hello" ,"Hello", "cái kẹo" , "đầu moi"}
myset = {True , 1 , 2, "banana"}
print(thisset)
print(myset)
#Trong set thì True và 1 là cùng một giá trị
#Trong set False và 0 là cùng 1 giá trị
print(len(myset))
print(type(myset))
thisset = set(("quả táo" , "quả cam" , "con cá"))
print(thisset)
#dictionary{
#              }  --> lệnh dict
#dictionary có thể sắp xếp theo thứ tự
#có thể thay đổi được nhưng ko đc lặp kí tự
#từ khóa:giá trị -->đi theo cặp
sinh_vien = {
    "tên": "Đồng Tố Chiến",
    "lớp": "Tiếng anh trans6",
    "ngành": "AI",
    "sinh năm": 2006
}
print(sinh_vien)
print(len(sinh_vien))
nganh_hoc_yeu_thich = {
   "ngành IT" : "lập trình máy tính",
   "ngành social":"marketing",
   "ngành kinh doanh":"quản trị kinh doanh",
   "các loại màu": ["đỏ","xanh","vàng"]
 }
print(nganh_hoc_yeu_thich)
print(type(nganh_hoc_yeu_thich))
thisdict = dict(name="Chien" , age = 36, country ="Vietnam")
print(thisdict)
#Bài tập Python
thanh_vien = ["chiến" , "an" ,"bình"]
thanh_vien.append("Dũng")
print(len(thanh_vien))
#Bài tập Python 2
clb_info = ("Hà Nội", 2024)
 #clb_info[1] = (2025)
#Bài tập Python 3
profile = {
    "ten":"Chien",
    "tuoi": 17,
    "ngon_ngu":"Viet nam"

}
print(profile)
profile["trang_thai"] = "Đang hoạt động"
profile["tuoi"] +=1
print(profile)
#Bài tập về set
so_thich = {"code" , "game" , "code" ,"bóng đá"}
print(so_thich)
so_thich.add("AI")
so_thich.remove("game")
print(so_thich)






