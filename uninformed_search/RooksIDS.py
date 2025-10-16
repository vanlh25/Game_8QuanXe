import time

BOARD_SIZE = 8

class RooksIDS:
    def __init__(self):
        self.initial_board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.goal_positions = [7, 0, 6, 2, 5, 1, 3, 4]

        # Thống kê
        self.find_goal = False
        self.tong_tt_dasinh = 0
        self.tong_tt_popped = 0
        self.tong_sobuoc = 0
        self.execution_time = 0

    def la_trang_thai_dich(self, board):
        return all(board[i][self.goal_positions[i]] == 1 for i in range(BOARD_SIZE))

    def sinh_trang_thai_con(self, board, hang_hien_tai):
        danh_sach_con = []
        for cot in range(BOARD_SIZE):
            if all(board[h][cot] == 0 for h in range(BOARD_SIZE)):
                new_board = [row[:] for row in board]
                new_board[hang_hien_tai][cot] = 1
                danh_sach_con.append(new_board)
        self.tong_tt_dasinh += len(danh_sach_con)
        return danh_sach_con

    def DLS(self, board, hang_hien_tai, limit, popped_boards):
        popped_boards.append([row[:] for row in board])
        self.tong_tt_popped += 1

        if self.la_trang_thai_dich(board):
            self.find_goal = True
            self.tong_sobuoc = self.tong_tt_popped
            return board

        if hang_hien_tai == BOARD_SIZE:
            return 'failure'

        if limit == 0:
            return 'cutoff'

        cutoff_occurred = False
        children = self.sinh_trang_thai_con(board, hang_hien_tai)
        for child_board in children:
            result = self.DLS(child_board, hang_hien_tai + 1, limit - 1, popped_boards)
            if result == 'cutoff':
                cutoff_occurred = True
            elif result != 'failure':
                return result

        if cutoff_occurred:
            return 'cutoff'
        else:
            return 'failure'

    def ids_pop_boards(self):
        start_time = time.time()
        self.find_goal = False
        self.tong_tt_dasinh = 0
        self.tong_tt_popped = 0
        self.tong_sobuoc = 0

        popped_boards = []
        for limit in range(1, BOARD_SIZE + 1):
            result = self.DLS(self.initial_board, 0, limit, popped_boards)
            if result != 'cutoff' and result != 'failure':
                break

        self.execution_time = round(time.time() - start_time, 2)
        return popped_boards

    def thong_so(self):
        return {
            "Tìm được lời giải": self.find_goal,
            "Tổng trạng thái sinh ra": self.tong_tt_dasinh,
            "Tổng trạng thái lấy ra": self.tong_tt_popped,
            "Bước đến lời giải": self.tong_sobuoc,
            "Thời gian chạy (giây)": self.execution_time,
        }
