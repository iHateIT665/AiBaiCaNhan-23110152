# AiBaiCaNhan-23110152
bài cá nhân dùng các thuật toán đã học để mô tả cách giải bài toán 8 hậu(Có làm ac-3)

Cấu trúc dự án như sau:
-File main ghi logic các nút để gọi thuật toán
-File ui thiết kế giao diện, các nút, vẽ bàn cờ
-Folder algorithms chứa các thuật toán trả về solution hoặc False
-File utils có các hàm hỗ trợ, các hàm observe để ghi lại thông tin thuật toán khi chạy vào file ixt.txt
Các nút thuật toán khi ấn vào thì bàn cờ bên trái sẽ mô tả cách đi đến bàn cờ solution bên phải
Nếu khi ấn bên phải không có bàn cờ nghĩa là thuật toán thất bại trong việc tìm lời giải

BFS,DFS,UCS khi ấn lần lượt sẽ sinh ra solution 1, 2, 3,...
DLS sẽ sinh ra solution lần 1 ,2 ,3 với limit = 7 (bàn cờ có 7 hậu)
IDS chỉ gọi DLS nên chỉ sinh đến khi có 1 solution
greedy và a* sẽ có bàn cờ mẫu solution bên phải và mỗi nước sẽ tính cost theo bàn cờ đó
HC,BEAM,SA đầu vào là bàn cờ random có sẵn 8 hậu trên 8 hàng, mục tiêu là tìm bàn cờ solution đầu tiên nhìn thấy
Andor sẽ chạy 1 lần tìm hết solution, nên sẽ không ghi solution ở bàn cờ phải
Không nhìn thấy sẽ có bàn cờ rỗng và chạy đến khi có tất cả solution
Nhìn thấy 1 phần bắt đầu với 1 bàn cờ có sẵn 2 quân hậu ở 2 hàng đầu và tìm 1 hoặc các solution từ đó

Thuật toán ac-3 với đầu vào em chọn là bàn cờ 2 vị trí hậu 0,1 đă đặt sẵn hợp lệ
Em chọn các tập là các hàng, mỗi hàng sẽ có domain tương ứng, ban đầu thì hàng 0 và 1 sẽ có 1 phần tử là vị trí đã chọn khởi tạo, các hàng còn lại có domain là 8 phần tử tương ứng 8 cột
Khởi tạo cung: các cung sẽ là 2,1 1,2 2,0 0,2,..., có tất cả 56 cung
Em xét từng cung và lọc khỏi domain từng hàng những giá trị không thỏa
Nếu có cung rỗng thì thuật toán AC-3 thất bại
Ngược lại thì sẽ dùng backtrack để tạo solution từ các domain đã được lọc


