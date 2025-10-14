import numpy as np
import math
import random

BOARD_SIZE = 8
GOAL = [7, 0, 6, 2, 5, 1, 3, 4]  # trạng thái mục tiêu (tùy bài toán)

class RooksSimulatedAnnealing:
    def __init__(self):
        self.goalboard = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        for i in range(BOARD_SIZE):
            self.goalboard[i][GOAL[i]] = 1

    def la_trang_thai_dich(self, board):
        return np.array_equal(board, self.goalboard)

    def cost_heuristic(self, board):
        """Giá trị đánh giá: càng cao càng tốt"""
        cols = np.argmax(board, axis=1)  # cột của mỗi xe
        unique_cols = len(set(cols))
        # số cặp xe không cùng cột = tổng cặp - số cặp trùng
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
        boards = []

        current = self.tao_trang_thai_ngau_nhien()
        E_current = self.cost_heuristic(current)
        boards.append(current.copy())

        T = 50.0      # nhiệt độ ban đầu
        alpha = 0.95  # tốc độ làm nguội
        iteration = 0

        while T > 1e-6 and iteration < 10000:
            if self.la_trang_thai_dich(current):
                break

            next_state = self.sinh_lan_can(current)
            E_next = self.cost_heuristic(next_state)
            deltaE = E_next - E_current

            # nếu tốt hơn hoặc chấp nhận theo xác suất e^(ΔE/T)
            if deltaE > 0 or math.exp(deltaE / T) > random.random():
                current = next_state
                E_current = E_next
                boards.append(current.copy())

            T *= alpha
            iteration += 1

        return boards
