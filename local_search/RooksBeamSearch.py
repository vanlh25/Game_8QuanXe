import math
import random
import numpy as np
import time

BOARD_SIZE = 8
GOAL = [7, 0, 6, 2, 5, 1, 3, 4]

class RooksBeamSearch:
    def __init__(self, beam_width=8):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.goalboard = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        for i in range(BOARD_SIZE):
            self.goalboard[i][GOAL[i]] = 1
        self.beam_width = beam_width

        # Thống kê
        self.find_goal = False
        self.tong_tt_dasinh = 0
        self.tong_tt_popped = 0
        self.tong_sobuoc = 0
        self.execution_time = 0
        self.board_cuoi = None  # Lưu trạng thái cuối cùng

    def la_trang_thai_dich(self, board):
        return np.array_equal(board, self.goalboard)

    def cost(self, board):
        flat = np.argmax(board, axis=1)
        N = len(flat)
        tong_cap = N * (N - 1) // 2
        tong_xe_moihang = np.bincount(flat, minlength=N)
        tong_captrung = np.sum(tong_xe_moihang * (tong_xe_moihang - 1) // 2)
        return tong_cap - tong_captrung

    def sinh_trang_thai_con(self, board, hang_hientai):
        danh_sach_con = []
        for cot in range(BOARD_SIZE):
            new_board = board.copy()
            new_board[hang_hientai, :] = 0
            new_board[hang_hientai, cot] = 1
            chi_phi_con = self.cost(new_board)
            danh_sach_con.append((new_board, chi_phi_con))
        return danh_sach_con

    def beamSearch_pop_boards(self):
        start_time = time.time()
        poped_boards = [self.board.copy()]
        hang_hientai = 0
        lst_ungvien = [(self.board.copy(), self.cost(self.board))]

        self.tong_tt_dasinh = 1
        self.tong_tt_popped = 1
        self.tong_sobuoc = 0

        while hang_hientai < BOARD_SIZE:
            # Kiểm tra goal
            for board_, _ in lst_ungvien:
                if self.la_trang_thai_dich(board_):
                    poped_boards.append(board_)
                    self.find_goal = True
                    self.execution_time = round(time.time() - start_time, 2)
                    self.board_cuoi = board_.copy()
                    return poped_boards

            # Sinh trạng thái con
            tmp_lst_ungvien = []
            for board_, cost in lst_ungvien:
                tmp_lst_ungvien.extend(self.sinh_trang_thai_con(board_, hang_hientai))
            self.tong_tt_dasinh += len(tmp_lst_ungvien)

            if not tmp_lst_ungvien:
                break

            # Chọn top beam
            costs = np.array([cost for _, cost in tmp_lst_ungvien])
            indices_sorted = np.argsort(-costs)
            top_indices = indices_sorted[:self.beam_width]
            lst_ungvien = [tmp_lst_ungvien[i] for i in top_indices]

            # Lưu các board đã pop
            for board_, _ in lst_ungvien:
                if not any(np.array_equal(board_, b) for b in poped_boards):
                    poped_boards.append(board_.copy())
                    self.tong_tt_popped += 1
                    self.tong_sobuoc += 1
                    self.board_cuoi = board_.copy()

            hang_hientai += 1

        self.execution_time = round(time.time() - start_time, 2)
        return poped_boards

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
