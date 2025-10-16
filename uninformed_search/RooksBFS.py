from collections import deque
import time

BOARD_SIZE = 8

class RooksBFS:
    def __init__(self):
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.GOAL = [0, 1, 2, 3, 6, 4, 5, 7]

        # Các thuộc tính để lưu thông số
        self.find_goal = False
        self.tong_tt_dasinh = 0
        self.tong_tt_popped = 0
        self.tong_sobuoc = 0
        self.max_queue_len = 0
        self.execution_time = 0

    def la_trang_thai_dich(self, board):
        return (
            board[0][0] == 1 and
            board[1][1] == 1 and
            board[2][2] == 1 and
            board[3][3] == 1 and
            board[4][6] == 1 and
            board[5][4] == 1 and
            board[6][5] == 1 and
            board[7][7] == 1
        )

    def sinh_trang_thai_con(self, board, hang_hien_tai):
        danh_sach_con = []
        for cot in range(BOARD_SIZE):
            if all(board[h][cot] == 0 for h in range(BOARD_SIZE)):
                new_board = [row[:] for row in board]
                new_board[hang_hien_tai][cot] = 1
                danh_sach_con.append(new_board)
        return danh_sach_con

    # Hàm BFS cũ nhưng ghi nhận thông số vào self
    def bfs_pop_boards(self):
        start_time = time.time()
        queue = deque([(self.board, 0)])
        popped_boards = []

        self.tong_tt_dasinh = 0
        self.tong_tt_popped = 0
        self.find_goal = False
        self.tong_sobuoc = 0
        self.max_queue_len = 1

        while queue:
            board, hang_hien_tai = queue.popleft()
            self.tong_tt_popped += 1

            # Lưu lại trạng thái đã lấy ra
            popped_boards.append([row[:] for row in board])

            if hang_hien_tai == BOARD_SIZE:
                if self.la_trang_thai_dich(board):
                    self.find_goal = True
                    self.tong_sobuoc = self.tong_tt_popped
                    break
                continue

            children = self.sinh_trang_thai_con(board, hang_hien_tai)
            self.tong_tt_dasinh += len(children)

            for child in children:
                queue.append((child, hang_hien_tai + 1))

            if len(queue) > self.max_queue_len:
                self.max_queue_len = len(queue)

        end_time = time.time()
        self.execution_time = end_time - start_time

        return popped_boards

    # Hàm thong_so chỉ trả về dict dựa trên các giá trị self đã ghi nhận
    def thong_so(self):
        return {
            "Tìm được lời giải": self.find_goal,
            "Tổng trạng thái sinh ra": self.tong_tt_dasinh,
            "Tổng trạng thái lấy ra": self.tong_tt_popped,
            "Bước đến lời giải": self.tong_sobuoc,
            "Độ dài hàng đợi tối đa": self.max_queue_len,
            "Thời gian chạy (giây)": round(self.execution_time, 2),
        }
