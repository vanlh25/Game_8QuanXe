import time

BOARD_SIZE = 8

class RooksDFS:
    def __init__(self):
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        # Các thông số
        self.find_goal = False
        self.tong_tt_dasinh = 0
        self.tong_tt_popped = 0
        self.tong_sobuoc = 0
        self.max_stack_len = 0
        self.execution_time = 0

    def la_trang_thai_dich(self, board):
        return (
                board[0][7] == 1 and
                board[1][0] == 1 and
                board[2][6] == 1 and
                board[3][2] == 1 and
                board[4][5] == 1 and
                board[5][1] == 1 and
                board[6][3] == 1 and
                board[7][4] == 1
        )

    def sinh_trang_thai_con(self, board, hang_hien_tai):
        danh_sach_con = []
        for cot in range(BOARD_SIZE):
            if all(board[h][cot] == 0 for h in range(BOARD_SIZE)):
                new_board = [row[:] for row in board]
                new_board[hang_hien_tai][cot] = 1
                danh_sach_con.append(new_board)
        return danh_sach_con

    def dfs_pop_boards(self):
        start_time = time.time()
        stack = [(self.board, 0)]
        popped_boards = []

        self.tong_tt_dasinh = 0
        self.tong_tt_popped = 0
        self.find_goal = False
        self.tong_sobuoc = 0
        self.max_stack_len = 1

        while stack:
            board, hang_hien_tai = stack.pop()
            self.tong_tt_popped += 1
            popped_boards.append([row[:] for row in board])

            if hang_hien_tai == BOARD_SIZE:
                if self.la_trang_thai_dich(board):
                    self.find_goal = True
                    self.tong_sobuoc = self.tong_tt_popped
                    break
                continue

            children = self.sinh_trang_thai_con(board, hang_hien_tai)
            self.tong_tt_dasinh += len(children)

            for child in reversed(children):
                stack.append((child, hang_hien_tai + 1))

            if len(stack) > self.max_stack_len:
                self.max_stack_len = len(stack)

        self.execution_time = round(time.time() - start_time, 2)
        return popped_boards

    def thong_so(self):
        return {
            "Tìm được lời giải": self.find_goal,
            "Tổng trạng thái sinh ra": self.tong_tt_dasinh,
            "Tổng trạng thái lấy ra": self.tong_tt_popped,
            "Bước đến lời giải": self.tong_sobuoc,
            "Độ dài stack tối đa": self.max_stack_len,
            "Thời gian chạy (giây)": self.execution_time,
        }
