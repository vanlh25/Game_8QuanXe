# ÁP DỤNG CÁC THUẬT TOÁN TÌM KIẾM VÀO GAME 8 QUÂN XE
## 1. Mô tả về bài toán
Bài toán 8 quân Xe (8 Rooks Problem) yêu cầu đặt 8 quân Xe trên bàn cờ 8x8 sao cho không có hai quân Xe nào tấn công nhau (không cùng hàng hoặc cột).
Dự án này triển khai 5 nhóm thuật toán tìm kiếm trong Trí tuệ Nhân tạo (AI Search Algorithms) để giải bài toán, so sánh hiệu quả và cách tiếp cận khác nhau.
## 2. Mục tiêu
- Hiểu rõ cách hoạt động của các thuật toán tìm kiếm đường đi ngắn nhất trong AI.
- Thực hành triển khai các thuật toán trên cùng một bài toán cụ thể.
- So sánh được hiệu suất ưu nhược điểm của thuật toán trong các bài toán khác nhau, dựa vào đó áp dụng vào thực tế.
- Làm nền tảng cho các vấn đề phức tạp hơn.
## 3. Nội dung báo cáo
### 3.1. Các thành phần chính có trong 8 Quân xe
- Trạng thái (State): Một trạng thái là một cấu hình gồm 8 quân xe được đặt trên bàn cờ 8x8. Trạng thái là tập các giá trị bàn cờ có thể có khi chơi 8 quân xe, có thể là bàn cờ trống, bàn cờ đặt một vài quân xe hoặc là đầy đủ quân xe
- Trạng thái ban đầu (Initial State): Có thể là một bàn cờ trống hoặc một cấu hình ngẫu nhiên của các quân xe.
- Trạng thái đích (Goal State): Là cấu hình mà tất cả 8 quân xe đều được đặt hợp lệ — tức không quân nào tấn công nhau hoặc là một bàn cờ đích cố định thỏa điều kiện đó.
- Hành động (Actions): Di chuyển một quân xe từ vị trí hiện tại sang một vị trí khác trên cùng hàng hoặc cột.
- Hàm kiểm tra mục tiêu (Goal Test): Kiểm tra xem có tồn tại hai quân xe nào nằm cùng hàng hoặc cùng cột hay không. Nếu không có, trạng thái hiện tại là trạng thái đích.
## 3.2. Các nhóm thuật toán
Nhóm thuật toán này còn gọi là tìm kiếm mù, nghĩa là thuật toán sẽ không biết trước trạng thái nào gần đích hơn. Nó chỉ dựa vào cấu trúc của không gian trạng thái và mở rộng các trạng thái một cách tuần tự. Với bài toán 8 Quân Xe, các thuật toán này sẽ lần lượt thử đặt quân Xe theo các cách khác nhau, từ trạng thái ban đầu (bàn cờ trống hoặc một vài quân Xe đã đặt) đến khi tìm ra cấu hình hợp lệ với 8 quân Xe.
#### 3.2.1. Uninformed Search (Tìm kiếm không thông tin - Tìm kiếm mù)
##### a. Breadth-First Search (BFS)
Mô tả: BFS là thuật toán tìm kiếm theo mức (level-order) trong không gian trạng thái. Trong bài toán 8 Quân Xe, BFS mở rộng tất cả các cấu hình quân Xe có thể đặt ở hàng hiện tại trước khi sang hàng tiếp theo. Thuật toán đảm bảo rằng khi tìm thấy cấu hình hợp lệ với 8 quân Xe, đó là lời giải với số bước di chuyển tối thiểu.
Cách thực hiện:
  - Bắt đầu từ trạng thái ban đầu (bàn cờ trống hoặc cấu hình ngẫu nhiên).
  - Sử dụng hàng đợi (Queue – FIFO) để lưu các trạng thái cần mở rộng.
  - Lần lượt mở rộng từng trạng thái: đặt thêm một quân Xe ở vị trí hợp lệ trên hàng tiếp theo, sinh ra các trạng thái con, thêm vào hàng đợi.
  - Kiểm tra trạng thái con với Goal Test: tất cả 8 quân Xe đều đặt hợp lệ (không cùng hàng, không cùng cột).
  - Lưu các trạng thái đã duyệt để tránh lặp vô hạn.
Ưu điểm:
  - Đảm bảo tìm được cấu hình hợp lệ tối ưu về số bước đặt quân Xe.
  - Hoạt động ổn định, dễ cài đặt.
Nhược điểm:
  - Tốn nhiều bộ nhớ khi không gian trạng thái lớn (nhiều khả năng đặt quân Xe).
  - Chậm nếu số lượng cấu hình khả thi quá nhiều.
##### b. Depth-First Search (DFS)
Mô tả:
DFS mở rộng các trạng thái theo chiều sâu trước, nghĩa là sẽ cố gắng đặt quân Xe vào các hàng tiếp theo cho đến khi đạt được cấu hình đầy đủ hoặc gặp bế tắc. Khi không thể đặt thêm quân Xe hợp lệ, thuật toán quay lui để thử các vị trí khác.
Cách thực hiện:
Bắt đầu với bàn cờ trống.
Đặt một quân Xe vào một ô hợp lệ trong hàng đầu tiên.
Đệ quy đặt tiếp các quân Xe vào các hàng kế tiếp.
Nếu không thể đặt quân Xe nào hợp lệ ở hàng hiện tại → quay lui (backtrack).
Nếu tất cả 8 hàng đều có quân Xe hợp lệ → tìm được nghiệm.
Ưu điểm:
*Sử dụng ít bộ nhớ hơn BFS.
*Dễ cài đặt với đệ quy.
Nhược điểm:
Có thể đi vào các nhánh sâu nhưng sai, tốn thời gian nếu không có giải pháp sớm.
Không đảm bảo tìm được nghiệm tối ưu.
##### c. Iterative Deepening Search (IDS)
##### d. Depth-Limited Search (DLS)
##### e. Uniform Cost Search (UCS)

#### 3.2.2. Informed Search (Tìm kiếm có thông tin)
Nhóm thuật toán này sử dụng thông tin bổ sung, gọi là heuristic, để ước lượng trạng thái nào có khả năng gần mục tiêu hơn. Thay vì mở rộng tất cả các trạng thái như nhóm Uninformed, các thuật toán trong nhóm này sẽ ưu tiên những trạng thái tốt hơn.
##### a. Greedy Best-First Search
##### b. A* Search

#### 3.2.3. Local Search (Tìm kiếm cục bộ)
Thuật toán tìm kiếm cục bộ không quan tâm đến toàn bộ đường đi, mà chỉ bắt đầu từ một trạng thái hiện tại và thử cải thiện nó bằng các thay đổi nhỏ quanh trạng thái đó.
##### a. Hill Climbing
##### b. Beam Search
##### c. Simulated Annealing
##### d. Genetic Algorithm (GA)

#### 3.2.4. Complex Environment Search (Môi trường phức tạp)
Nhóm này áp dụng cho các môi trường mà trạng thái tiếp theo phụ thuộc vào nhiều điều kiện hoặc thông tin không đầy đủ.
Ví dụ, nếu bài toán 8 Quân Xe mở rộng thành một môi trường “phức tạp” có nhiều người chơi, hoặc mỗi quân Xe có thêm điều kiện di chuyển khác, thuật toán phải tính toán nhiều khả năng trước khi quyết định bước đi. 
##### a. AND-OR Search
##### b. Belief Search
##### c. Partial Observation
#### 3.2.5. Constraint Satisfaction Problem Search (Tìm kiếm thỏa mãn ràng buộc)
Nhóm này dùng khi bài toán có ràng buộc rõ ràng, ví dụ trong 8 Quân Xe, không hai quân Xe được cùng hàng hoặc cùng cột.

Ý tưởng là thử gán giá trị cho các biến (ví dụ: vị trí của từng quân Xe) sao cho không vi phạm ràng buộc. 
##### a. Backtracking
##### b. Forward Checking
##### c. AC-3
