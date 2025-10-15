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
## 3.2. Các nhóm thuật toán và minh họa gif các thuật toán
Nhóm thuật toán này còn gọi là tìm kiếm mù, nghĩa là thuật toán sẽ không biết trước trạng thái nào gần đích hơn. Nó chỉ dựa vào cấu trúc của không gian trạng thái và mở rộng các trạng thái một cách tuần tự. Với bài toán 8 Quân Xe, các thuật toán này sẽ lần lượt thử đặt quân Xe theo các cách khác nhau, từ trạng thái ban đầu (bàn cờ trống hoặc một vài quân Xe đã đặt) đến khi tìm ra cấu hình hợp lệ với 8 quân Xe.
#### 3.2.1. Uninformed Search (Tìm kiếm không thông tin - Tìm kiếm mù)
##### a. Breadth-First Search (BFS)
Mô tả: BFS là thuật toán tìm kiếm theo mức (level-order) trong không gian trạng thái. Trong bài toán 8 Quân Xe, BFS mở rộng tất cả các cấu hình quân Xe có thể đặt ở hàng hiện tại trước khi sang hàng tiếp theo. Thuật toán đảm bảo rằng khi tìm thấy cấu hình hợp lệ với 8 quân Xe, đó là lời giải với số bước di chuyển tối thiểu.
##### b. Depth-First Search (DFS)
Mô tả: DFS mở rộng các trạng thái theo chiều sâu trước, nghĩa là sẽ cố gắng đặt quân Xe vào các hàng tiếp theo cho đến khi đạt được cấu hình đầy đủ hoặc gặp bế tắc. Khi không thể đặt thêm quân Xe hợp lệ, thuật toán quay lui để thử các vị trí khác. Cách thực hiện:
##### c. Iterative Deepening Search (IDS)
Mô tả:
IDS là sự kết hợp giữa BFS và DFS. Thuật toán thực hiện nhiều lần tìm kiếm DFS, mỗi lần tăng giới hạn độ sâu thêm 1 cho đến khi tìm thấy lời giải. IDS đảm bảo tìm được nghiệm tối ưu trong khi vẫn tiết kiệm bộ nhớ.
##### d. Depth-Limited Search (DLS)
Mô tả: DLS là biến thể của DFS nhưng có giới hạn độ sâu tối đa, giúp tránh việc tìm kiếm vô tận trong không gian trạng thái lớn. Trong bài toán 8 Quân Xe, độ sâu tối đa thường là 8 (tương ứng với 8 hàng của bàn cờ).
##### e. Uniform Cost Search (UCS)
Mô tả:
UCS mở rộng trạng thái theo chi phí nhỏ nhất. Mỗi bước đặt quân Xe được xem là một hành động có chi phí (thường là 1). UCS đảm bảo tìm được lời giải có tổng chi phí thấp nhất, tương đương với số bước đặt quân tối thiểu.
#### 3.2.2. Informed Search (Tìm kiếm có thông tin)
Nhóm thuật toán này sử dụng thông tin bổ sung, gọi là heuristic, để ước lượng trạng thái nào có khả năng gần mục tiêu hơn. Thay vì mở rộng tất cả các trạng thái như nhóm Uninformed, các thuật toán trong nhóm này sẽ ưu tiên những trạng thái tốt hơn.
##### a. Greedy Best-First Search
Mô tả:
Greedy Best-First Search chọn trạng thái có giá trị heuristic nhỏ nhất, nghĩa là trạng thái được ước lượng gần mục tiêu hơn. Trong bài toán 8 Quân Xe, giá trị heuristic có thể là số lượng cặp quân Xe đang tấn công nhau (cùng hàng hoặc cột).
##### b. A* Search
A* là thuật toán kết hợp giữa chi phí thực tế và ước lượng heuristic. Nó sử dụng hàm đánh giá:
- f(n) = g(n) + h(n)
- Trong đó g(n) là chi phí thực tế (số quân Xe đã đặt hợp lệ), còn h(n) là số lượng xung đột còn lại cần giải quyết.
#### 3.2.3. Local Search (Tìm kiếm cục bộ)
Thuật toán tìm kiếm cục bộ không quan tâm đến toàn bộ đường đi, mà chỉ bắt đầu từ một trạng thái hiện tại và thử cải thiện nó bằng các thay đổi nhỏ quanh trạng thái đó.
##### a. Hill Climbing
Mô tả:
Hill Climbing là thuật toán tìm kiếm cục bộ bắt đầu từ một cấu hình ngẫu nhiên, sau đó liên tục cải thiện bằng cách giảm số lượng xung đột giữa các quân Xe. Thuật toán dừng khi không thể cải thiện thêm.
##### b. Beam Search
Mô tả:
Beam Search mở rộng đồng thời nhiều trạng thái, nhưng chỉ giữ lại một số lượng hữu hạn trạng thái tốt nhất tại mỗi bước (beam width = k).
##### c. Simulated Annealing
Mô tả:
Simulated Annealing là phiên bản cải tiến của Hill Climbing, cho phép chấp nhận tạm thời các bước đi xấu hơn với xác suất giảm dần theo nhiệt độ T để tránh bị mắc kẹt ở cực trị địa phương.
##### d. Genetic Algorithm (GA)
Mô tả:
GA mô phỏng quá trình tiến hóa sinh học. Mỗi cấu hình bàn cờ là một cá thể trong quần thể, và thuật toán chọn lọc, lai ghép, đột biến để tạo ra thế hệ mới tốt hơn.

#### 3.2.4. Complex Environment Search (Môi trường phức tạp)
Nhóm này áp dụng cho các môi trường mà trạng thái tiếp theo phụ thuộc vào nhiều điều kiện hoặc thông tin không đầy đủ.
Ví dụ, nếu bài toán 8 Quân Xe mở rộng thành một môi trường “phức tạp” có nhiều người chơi, hoặc mỗi quân Xe có thêm điều kiện di chuyển khác, thuật toán phải tính toán nhiều khả năng trước khi quyết định bước đi. 
##### a. AND-OR Search
Mô tả:
AND-OR Search được dùng trong các bài toán có nhiều lựa chọn (OR) và nhiều điều kiện phải thỏa mãn đồng thời (AND). Trong bài toán 8 Quân Xe mở rộng, một bước di chuyển có thể dẫn đến nhiều tình huống cần xử lý cùng lúc

##### b. Belief Search
Mô tả:
Belief Search được sử dụng khi trạng thái của bàn cờ không xác định hoàn toàn (chỉ biết một số quân Xe chắc chắn đúng vị trí). Thuật toán duy trì tập hợp các trạng thái có thể xảy ra (belief states) và cập nhật chúng sau mỗi hành động.

##### c. Partial Observation
Mô tả:
Partial Observation được áp dụng khi không thể quan sát toàn bộ bàn cờ (ví dụ, chỉ thấy một phần vị trí quân Xe). Thuật toán dựa trên thông tin hiện có để suy luận bước đi tiếp theo.

#### 3.2.5. Constraint Satisfaction Problem Search (Tìm kiếm thỏa mãn ràng buộc)
Nhóm này dùng khi bài toán có ràng buộc rõ ràng, ví dụ trong 8 Quân Xe, không hai quân Xe được cùng hàng hoặc cùng cột.

Ý tưởng là thử gán giá trị cho các biến (ví dụ: vị trí của từng quân Xe) sao cho không vi phạm ràng buộc. 
##### a. Backtracking
Mô tả:
Backtracking là phương pháp thử - sai có kiểm soát. Thuật toán đặt từng quân Xe vào hàng, kiểm tra tính hợp lệ, và quay lui khi gặp xung đột.

##### b. Forward Checking
Mô tả:
Forward Checking mở rộng Backtracking bằng cách loại bỏ sớm các giá trị không hợp lệ của những quân Xe chưa được đặt.

##### c. AC-3
Mô tả:
AC-3 (Arc Consistency Algorithm 3) đảm bảo tính nhất quán của các ràng buộc nhị phân giữa các biến. Trong 8 Quân Xe, ràng buộc là “hai quân Xe không được ở cùng cột”.

## 3.3. Kết luận
Các thuật toán đều có các ưu và nhược điểm riêng sẽ phù hợp trong các ngữ cảnh khác nhau
Kết quả thuật toán có thể là không tìm ra kết quả chẳng hạn đặc biệt là các thuật toán Local Search và các thuật toán trong môi trường phức tạp.
