import time

BOARD_SIZE = 8

class RooksDLS:
    def __init__(self):
        self.initial_board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        # Thống kê
        self.find_goal = False
        self.tong_tt_dasinh = 0
        self.tong_tt_popped = 0
        self.tong_sobuoc = 0
        self.max_depth = 0
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
        self.tong_tt_dasinh += len(danh_sach_con)
        return danh_sach_con

    def DLS(self, board, hang_hien_tai, limit, popped_boards, depth):
        # Lưu trạng thái đã pop
        popped_boards.append([row[:] for row in board])
        self.tong_tt_popped += 1

        # Cập nhật max depth
        if depth > self.max_depth:
            self.max_depth = depth

        # Kiểm tra goal
        if self.la_trang_thai_dich(board):
            self.find_goal = True
            self.tong_sobuoc = self.tong_tt_popped
            return board

        if limit == 0:
            return 'cutoff'

        cutoff_occurred = False
        children = self.sinh_trang_thai_con(board, hang_hien_tai)
        for child_board in children:
            result = self.DLS(child_board, hang_hien_tai + 1, limit - 1, popped_boards, depth + 1)
            if result == 'cutoff':
                cutoff_occurred = True
            elif result != 'failure':
                return result

        if cutoff_occurred:
            return 'cutoff'
        else:
            return 'failure'

    def depth_limited_search(self, limit=BOARD_SIZE):
        start_time = time.time()
        popped_boards = []
        # reset thông số
        self.find_goal = False
        self.tong_tt_dasinh = 0
        self.tong_tt_popped = 0
        self.tong_sobuoc = 0
        self.max_depth = 0

        self.DLS(self.initial_board, 0, limit, popped_boards, 1)
        self.execution_time = round(time.time() - start_time, 2)
        return popped_boards

    def thong_so(self):
        return {
            "Tìm được lời giải": self.find_goal,
            "Tổng trạng thái sinh ra": self.tong_tt_dasinh,
            "Tổng trạng thái lấy ra": self.tong_tt_popped,
            "Bước đến lời giải": self.tong_sobuoc,
            "Chiều sâu tối đa": self.max_depth,
            "Thời gian chạy (giây)": self.execution_time,
        }
