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
3.2.1. Uninformed Search (Tìm kiếm không thông tin - Tìm kiếm mù)
b. Depth-First Search (DFS)

Mô tả:
DFS mở rộng các trạng thái theo chiều sâu trước, nghĩa là sẽ cố gắng đặt quân Xe vào các hàng tiếp theo cho đến khi đạt được cấu hình đầy đủ hoặc gặp bế tắc. Khi không thể đặt thêm quân Xe hợp lệ, thuật toán quay lui để thử các vị trí khác.

Cách thực hiện:

Bắt đầu với bàn cờ trống.

Đặt một quân Xe vào một ô hợp lệ trong hàng đầu tiên.

Đệ quy đặt tiếp các quân Xe vào các hàng kế tiếp.

Nếu không thể đặt quân Xe nào hợp lệ ở hàng hiện tại → quay lui (backtrack).

Nếu tất cả 8 hàng đều có quân Xe hợp lệ → tìm được nghiệm.

Ưu điểm:

Sử dụng ít bộ nhớ hơn BFS.

Dễ cài đặt với đệ quy.

Nhược điểm:

Có thể đi vào các nhánh sâu nhưng sai, tốn thời gian nếu không có giải pháp sớm.

Không đảm bảo tìm được nghiệm tối ưu.

c. Depth-Limited Search (DLS)

Mô tả:
DLS là phiên bản của DFS nhưng có giới hạn độ sâu tối đa để tránh tìm kiếm quá sâu hoặc vô hạn.
Trong bài toán 8 quân Xe, độ sâu tối đa thường là 8 (tương ứng 8 hàng của bàn cờ).

Cách thực hiện:

Giống DFS, nhưng nếu đạt đến độ sâu giới hạn mà chưa có 8 quân Xe hợp lệ → dừng mở rộng.

Nếu đạt đủ 8 quân Xe → trả về lời giải.

Ưu điểm:

Tránh vòng lặp vô hạn.

Có thể điều chỉnh độ sâu tùy theo yêu cầu.

Nhược điểm:

Nếu giới hạn quá nhỏ → có thể bỏ sót nghiệm.

Nếu giới hạn quá lớn → trở lại như DFS.

d. Iterative Deepening Search (IDS)

Mô tả:
IDS kết hợp ưu điểm của BFS (đảm bảo tối ưu) và DFS (tiết kiệm bộ nhớ). Thuật toán thực hiện nhiều lần tìm kiếm DFS với độ sâu tăng dần (1, 2, 3, …, 8).
Khi đến độ sâu mà có lời giải, IDS sẽ dừng.

Cách thực hiện:

Đặt depth_limit = 1.

Thực hiện DLS với giới hạn đó.

Nếu không tìm được → tăng depth_limit lên 1.

Lặp lại cho đến khi tìm được cấu hình hợp lệ.

Ưu điểm:

Tìm được lời giải tối ưu.

Dùng ít bộ nhớ hơn BFS.

Nhược điểm:

Lặp lại nhiều lần các trạng thái ban đầu → tốn thời gian hơn BFS nếu không gian lớn.

e. Uniform Cost Search (UCS)

Mô tả:
UCS mở rộng các trạng thái theo chi phí nhỏ nhất. Với bài toán 8 quân Xe, mỗi bước đặt quân Xe có thể xem là một “chi phí” (ví dụ 1 đơn vị).
Thuật toán đảm bảo tìm được cấu hình hợp lệ với tổng chi phí nhỏ nhất.

Cách thực hiện:

Dùng hàng đợi ưu tiên (priority queue) để lưu trạng thái và chi phí.

Luôn mở rộng trạng thái có tổng chi phí nhỏ nhất.

Khi đạt cấu hình hợp lệ 8 quân Xe → dừng lại.

Ưu điểm:

Đảm bảo tìm được lời giải tối ưu về chi phí.

Tốt trong bài toán có trọng số.

Nhược điểm:

Chậm hơn BFS nếu tất cả chi phí như nhau.

Tốn bộ nhớ do phải lưu nhiều trạng thái.

3.2.2. Informed Search (Tìm kiếm có thông tin)
a. Greedy Best-First Search

Mô tả:
Greedy chọn trạng thái có hàm heuristic nhỏ nhất – ước lượng trạng thái đó gần mục tiêu hơn.
Heuristic trong bài toán 8 quân Xe có thể là số lượng xung đột giữa các quân Xe (số cặp quân cùng hàng hoặc cột).

Cách thực hiện:

Bắt đầu từ trạng thái ban đầu.

Tính giá trị heuristic h(n) cho từng trạng thái con.

Luôn mở rộng trạng thái có h(n) nhỏ nhất.

Khi h(n) = 0, tức không có xung đột → đạt trạng thái đích.

Ưu điểm:

Tìm kiếm nhanh hơn nhiều so với BFS.

Tập trung vào hướng có khả năng đúng.

Nhược điểm:

Có thể rơi vào bẫy cục bộ (local minimum).

Không đảm bảo tìm được nghiệm tối ưu.

b. A* Search

Mô tả:
A* kết hợp chi phí thực tế (g(n)) và ước lượng heuristic (h(n)) bằng công thức:

f(n) = g(n) + h(n)
Trong 8 quân Xe, g(n) là số quân đã đặt hợp lệ, còn h(n) là số xung đột còn lại.

Cách thực hiện:

Dùng hàng đợi ưu tiên lưu theo f(n).

Luôn mở rộng trạng thái có f(n) nhỏ nhất.

Khi h(n) = 0 và g(n) = 8 → đạt cấu hình hoàn chỉnh.

Ưu điểm:

Nhanh và hiệu quả nếu heuristic tốt.

Đảm bảo tìm nghiệm tối ưu nếu h(n) chấp nhận được (admissible).

Nhược điểm:

Tốn bộ nhớ khi không gian lớn.

3.2.3. Local Search (Tìm kiếm cục bộ)
a. Hill Climbing

Mô tả:
Bắt đầu từ một cấu hình ngẫu nhiên, Hill Climbing tìm cách giảm số xung đột bằng cách di chuyển một quân Xe để cải thiện trạng thái.

Cách thực hiện:

Sinh cấu hình ban đầu ngẫu nhiên.

Đánh giá h(n) = số cặp Xe tấn công nhau.

Di chuyển từng Xe để giảm h(n).

Nếu không thể giảm thêm → dừng (đỉnh cục bộ).

Ưu điểm:

Nhanh, tốn ít bộ nhớ.

Phù hợp với bài toán lớn.

Nhược điểm:

Dễ mắc kẹt ở cực trị địa phương (local maximum/minimum).

b. Beam Search

Mô tả:
Beam Search mở rộng đồng thời nhiều trạng thái tốt nhất (beam width = k).
Giữ lại k trạng thái có heuristic tốt nhất ở mỗi bước.

Cách thực hiện:

Sinh nhiều cấu hình ban đầu ngẫu nhiên.

Chỉ giữ k cấu hình tốt nhất (ít xung đột nhất).

Sinh tiếp các trạng thái con từ các cấu hình đó.

Lặp lại cho đến khi tìm được cấu hình không xung đột.

Ưu điểm:

Nhanh hơn BFS, hiệu quả hơn Hill Climbing.

Tránh được local minimum trong nhiều trường hợp.

Nhược điểm:

Có thể bỏ sót nghiệm do cắt tỉa mạnh.

c. Simulated Annealing

Mô tả:
Giống Hill Climbing nhưng cho phép chấp nhận tạm thời trạng thái xấu hơn với xác suất giảm dần (mô phỏng quá trình làm nguội kim loại).

Cách thực hiện:

Bắt đầu với cấu hình ngẫu nhiên và “nhiệt độ” T lớn.

Ở mỗi bước, chọn trạng thái láng giềng.

Nếu tốt hơn → chấp nhận; nếu xấu hơn → chấp nhận với xác suất exp(-ΔE/T).

Giảm T dần.

Khi T → 0, dừng lại.

Ưu điểm:

Có thể thoát khỏi bẫy cục bộ.

Hiệu quả cho các bài toán tối ưu hóa phức tạp.

Nhược điểm:

Cần tinh chỉnh tham số nhiệt độ.

d. Genetic Algorithm (GA)

Mô tả:
GA mô phỏng tiến hóa tự nhiên: mỗi cấu hình bàn cờ là một “cá thể”, thuật toán lai ghép và chọn lọc các cá thể tốt nhất.

Cách thực hiện:

Mỗi cá thể: mảng gồm 8 vị trí Xe.

Đánh giá fitness = số lượng Xe không tấn công nhau.

Lai ghép (crossover) và đột biến (mutation) để tạo thế hệ mới.

Lặp lại cho đến khi có cá thể có fitness = 8.

Ưu điểm:

Có thể tìm được nghiệm dù không gian tìm kiếm lớn.

Khả năng vượt qua local minimum cao.

Nhược điểm:

Tốn thời gian tính toán.

Kết quả không ổn định (phụ thuộc tham số).

3.2.4. Complex Environment Search (Môi trường phức tạp)
a. AND-OR Search

Mô tả:
Áp dụng khi có nhiều lựa chọn (OR) và nhiều điều kiện bắt buộc (AND).
Trong 8 quân Xe mở rộng (ví dụ nhiều người chơi hoặc ràng buộc đồng thời), thuật toán xác định cây tìm kiếm trong đó nút AND yêu cầu tất cả các nhánh con thỏa mãn, còn nút OR chỉ cần một nhánh con hợp lệ.

b. Belief Search

Mô tả:
Dùng khi trạng thái không xác định hoàn toàn (ví dụ chỉ biết một số quân Xe chắc chắn đúng vị trí, còn lại không rõ).
Thuật toán sẽ duy trì tập hợp các trạng thái có thể (belief states) và cập nhật chúng sau mỗi hành động.

c. Partial Observation

Mô tả:
Khi không thể quan sát toàn bộ bàn cờ, thuật toán tìm kiếm dựa vào thông tin từng phần (ví dụ, chỉ biết vị trí của một vài quân Xe).
Sử dụng suy luận xác suất hoặc tập hợp trạng thái khả dĩ để chọn hành động tốt nhất tiếp theo.

3.2.5. Constraint Satisfaction Problem Search (Tìm kiếm thỏa mãn ràng buộc)
a. Backtracking

Mô tả:
Là phương pháp phổ biến nhất cho bài toán 8 quân Xe.
Thử gán vị trí cho từng Xe theo hàng, và quay lui nếu vi phạm ràng buộc (cùng hàng/cột).

Cách thực hiện:

Gán vị trí cho Xe hàng đầu tiên.

Kiểm tra ràng buộc với các Xe trước đó.

Nếu hợp lệ → sang Xe kế tiếp.

Nếu vi phạm → quay lui và thử vị trí khác.

Ưu điểm:

Đơn giản, hiệu quả cho 8 quân Xe.

Đảm bảo tìm được tất cả nghiệm.

Nhược điểm:

Hiệu suất giảm mạnh khi mở rộng kích thước bàn cờ.

b. Forward Checking

Mô tả:
Cải tiến Backtracking bằng cách loại bỏ sớm các giá trị không thể trong tương lai.
Khi gán vị trí cho một Xe, loại bỏ tất cả vị trí cùng cột của các Xe sau đó.

Ưu điểm:

Giảm đáng kể số nhánh cần duyệt.

Phát hiện vi phạm sớm.

Nhược điểm:

Cần thêm chi phí lưu trữ miền giá trị.

c. AC-3 (Arc Consistency)

Mô tả:
Thuật toán kiểm tra tính nhất quán trên các ràng buộc nhị phân.
Trong 8 quân Xe, mỗi biến (Xe) có miền giá trị là các cột có thể đặt.
AC-3 sẽ loại bỏ các giá trị trong miền khiến hai Xe xung đột.

Cách thực hiện:

Mỗi ràng buộc (Xi, Xj) đảm bảo Xi ≠ Xj (không cùng cột).

Nếu phát hiện domain(Xi) trùng hoàn toàn với domain(Xj) → loại bỏ một giá trị.

Lặp lại cho đến khi không còn thay đổi.

Ưu điểm:

Giảm mạnh số miền giá trị trước khi tìm kiếm.

Kết hợp tốt với Backtracking.

Nhược điểm:

Tốn thời gian khởi tạo với nhiều ràng buộc.
