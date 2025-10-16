import numpy as np
import time

BOARD_SIZE = 8
GOAL = [7, 0, 6, 2, 5, 1, 3, 4]

class RooksHillClimbing:
    def __init__(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.goalboard = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        for i in range(BOARD_SIZE):
            self.goalboard[i][GOAL[i]] = 1

        # Thống kê
        self.find_goal = False
        self.tong_tt_dasinh = 0
        self.tong_tt_popped = 0
        self.tong_sobuoc = 0
        self.execution_time = 0
        self.board_cuoi = None  # Lưu trạng thái cuối cùng

    def la_trang_thai_dich(self, board):
        return np.array_equal(board, self.goalboard)

    def cost_heuristic(self, board):
        flat = np.argmax(board, axis=1)
        N = len(flat)
        tong_cap = N * (N - 1) // 2
        tong_xe_moihang = np.bincount(flat, minlength=N)
        tong_captrung = np.sum(tong_xe_moihang * (tong_xe_moihang - 1) // 2)
        return tong_cap - tong_captrung

    def sinh_trang_thai_con(self, board, hang_hientai):
        danh_sach_con = []
        for cot in range(BOARD_SIZE):
            new_board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
            new_board[:hang_hientai] = board[:hang_hientai]
            new_board[hang_hientai, cot] = 1
            chi_phi_con = self.cost_heuristic(new_board)
            danh_sach_con.append((new_board, chi_phi_con))
            self.tong_tt_dasinh += 1
        return danh_sach_con

    def hill_pop_boards(self):
        start_time = time.time()
        self.find_goal = False
        self.tong_tt_dasinh = 0
        self.tong_tt_popped = 0
        self.tong_sobuoc = 0

        poped_boards = []
        board_hientai = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

        for hang_hientai in range(BOARD_SIZE):
            lst_children = self.sinh_trang_thai_con(board_hientai, hang_hientai)
            costs = [cost for _, cost in lst_children]
            index_maxcost = np.argmax(costs)
            best_board, best_cost = lst_children[index_maxcost]

            poped_boards.append(best_board.copy())
            self.tong_tt_popped += 1

            current_cost = self.cost_heuristic(board_hientai)
            if best_cost <= current_cost:
                self.find_goal = self.la_trang_thai_dich(best_board)
                self.tong_sobuoc = self.tong_tt_popped
                self.board_cuoi = best_board.copy()
                self.execution_time = round(time.time() - start_time, 2)
                return poped_boards

            board_hientai = best_board.copy()

        self.find_goal = self.la_trang_thai_dich(board_hientai)
        self.board_cuoi = board_hientai.copy()
        self.tong_sobuoc = self.tong_tt_popped
        self.execution_time = round(time.time() - start_time, 2)
        return poped_boards

    def thong_so(self):
        ghi_chu = ""
        if self.board_cuoi is not None:
            # Kiểm tra hợp lệ: mỗi hàng và mỗi cột chỉ có 1 quân
            row_ok = all(sum(self.board_cuoi[i]) == 1 for i in range(BOARD_SIZE))
            col_ok = all(sum(self.board_cuoi[:, j]) == 1 for j in range(BOARD_SIZE))
            khac_goal = not np.array_equal(self.board_cuoi, self.goalboard)

            if row_ok and col_ok and khac_goal:
                ghi_chu = "Bàn cờ cuối thỏa ĐK 8 quân xe!"

        return {
            "Tìm được lời giải": self.find_goal,
            "Tổng trạng thái sinh ra": self.tong_tt_dasinh,
            "Tổng trạng thái lấy ra": self.tong_tt_popped,
            "Bước đến lời giải": self.tong_sobuoc,
            "Thời gian chạy (giây)": self.execution_time,
            "Note": ghi_chu
        }
