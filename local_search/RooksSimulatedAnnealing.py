import numpy as np
import math
import random
import time

BOARD_SIZE = 8
GOAL = [7, 0, 6, 2, 5, 1, 3, 4]

class RooksSimulatedAnnealing:
    def __init__(self):
        self.goalboard = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        for i in range(BOARD_SIZE):
            self.goalboard[i][GOAL[i]] = 1
        # Thông số
        self.find_goal = False
        self.tong_tt_dasinh = 0
        self.tong_tt_popped = 0
        self.tong_sobuoc = 0
        self.execution_time = 0
        self.board_cuoi = None  # Lưu trạng thái cuối cùng

    def la_trang_thai_dich(self, board):
        return np.array_equal(board, self.goalboard)

    def cost_heuristic(self, board):
        """Giá trị đánh giá: càng cao càng tốt"""
        cols = np.argmax(board, axis=1)
        unique_cols = len(set(cols))
        total_pairs = BOARD_SIZE * (BOARD_SIZE - 1) // 2
        same_col_pairs = BOARD_SIZE - unique_cols
        return total_pairs - same_col_pairs

    def sinh_lan_can(self, board):
        """Sinh trạng thái kế cận: di chuyển 1 xe sang cột khác"""
        new_board = board.copy()
        row = random.randint(0, BOARD_SIZE - 1)
        col = np.argmax(new_board[row])
        new_board[row, col] = 0
        new_col = random.choice([c for c in range(BOARD_SIZE) if c != col])
        new_board[row, new_col] = 1
        return new_board

    def tao_trang_thai_ngau_nhien(self):
        """Tạo 1 trạng thái ban đầu hợp lệ: mỗi hàng 1 xe"""
        board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        for i in range(BOARD_SIZE):
            col = random.randint(0, BOARD_SIZE - 1)
            board[i][col] = 1
        return board

    def simulatedAnnealing_pop_boards(self):
        """Thuật toán simulated annealing chuẩn"""
        start_time = time.time()
        boards = []

        current = self.tao_trang_thai_ngau_nhien()
        E_current = self.cost_heuristic(current)
        boards.append(current.copy())

        self.tong_tt_dasinh = 1
        self.tong_tt_popped = 1
        self.tong_sobuoc = 0

        T = 50.0
        alpha = 0.95
        iteration = 0

        while T > 1e-6 and iteration < 10000:
            if self.la_trang_thai_dich(current):
                self.find_goal = True
                break

            next_state = self.sinh_lan_can(current)
            E_next = self.cost_heuristic(next_state)
            deltaE = E_next - E_current

            if deltaE > 0 or math.exp(deltaE / T) > random.random():
                current = next_state
                E_current = E_next
                boards.append(current.copy())
                self.tong_tt_popped += 1
                self.tong_sobuoc += 1

            self.tong_tt_dasinh += 1
            T *= alpha
            iteration += 1

        self.board_cuoi = current.copy()
        self.execution_time = round(time.time() - start_time, 2)
        return boards

    def thong_so(self):
        ghi_chu = ""
        if self.board_cuoi is not None:
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
