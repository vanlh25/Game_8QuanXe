import time
from heapq import heappush, heappop

BOARD_SIZE = 8
GOAL_COLS = [7, 0, 6, 2, 5, 1, 3, 4]

class RooksGS:
    def __init__(self):
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        # Thống kê
        self.find_goal = False
        self.tong_tt_dasinh = 0
        self.tong_tt_popped = 0
        self.tong_sobuoc = 0
        self.execution_time = 0

    def la_trang_thai_dich(self, board):
        return all(board[i][GOAL_COLS[i]] == 1 for i in range(BOARD_SIZE))

    def chi_phi(self, hang_hien_tai, cot):
        return abs(GOAL_COLS[hang_hien_tai] - cot)

    def sinh_trang_thai_con(self, board, hang_hien_tai):
        children = []
        for cot in range(BOARD_SIZE):
            if all(board[h][cot] == 0 for h in range(BOARD_SIZE)):
                new_board = [row[:] for row in board]
                new_board[hang_hien_tai][cot] = 1
                chi_phi_con = self.chi_phi(hang_hien_tai, cot)
                children.append((new_board, chi_phi_con))
        self.tong_tt_dasinh += len(children)
        return children

    def gs_pop_boards(self):
        start_time = time.time()
        self.find_goal = False
        self.tong_tt_dasinh = 0
        self.tong_tt_popped = 0
        self.tong_sobuoc = 0

        heap = []
        heappush(heap, (0, self.board, 0))
        popped_boards = []

        while heap:
            chi_phi_hien_tai, board, hang_hien_tai = heappop(heap)
            popped_boards.append([row[:] for row in board])
            self.tong_tt_popped += 1

            if hang_hien_tai == BOARD_SIZE:
                if self.la_trang_thai_dich(board):
                    self.find_goal = True
                    self.tong_sobuoc = self.tong_tt_popped
                    break
                continue

            children = self.sinh_trang_thai_con(board, hang_hien_tai)
            for child_board, chi_phi_con in children:
                heappush(heap, (chi_phi_con, child_board, hang_hien_tai + 1))

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
