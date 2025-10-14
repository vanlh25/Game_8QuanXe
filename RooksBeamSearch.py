import math
import random
import numpy as np

BOARD_SIZE = 8
GOAL = [7, 0, 6, 2, 5, 1, 3, 4]

class RooksBeamSearch:
    def __init__(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.goalboard = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        for i in range(BOARD_SIZE):
            self.goalboard[i][GOAL[i]] = 1

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
            new_board[hang_hientai, :] = 0  # xóa hàng cũ
            new_board[hang_hientai, cot] = 1
            chi_phi_con = self.cost(new_board)
            danh_sach_con.append((new_board, chi_phi_con))
        return danh_sach_con

    def beamSearch_pop_boards(self):
        poped_boards = [self.board.copy()]
        beam = 8
        hang_hientai = 0
        lst_ungvien = [(self.board.copy(), self.cost(self.board))]

        while hang_hientai < BOARD_SIZE:
            for board_, cost in lst_ungvien:
                if self.la_trang_thai_dich(board_):
                    poped_boards.append(board_)
                    return poped_boards

            tmp_lst_ungvien = []
            for board_, cost in lst_ungvien:
                tmp_lst_ungvien.extend(self.sinh_trang_thai_con(board_, hang_hientai))

            if not tmp_lst_ungvien:
                return poped_boards

            costs = np.array([cost for _, cost in tmp_lst_ungvien])
            indices_sorted = np.argsort(-costs)
            top_indices = indices_sorted[:beam]
            lst_ungvien = [tmp_lst_ungvien[i] for i in top_indices]

            for board_, cost in lst_ungvien:
                if not any(np.array_equal(board_, b) for b in poped_boards):
                    poped_boards.append(board_.copy())

            hang_hientai += 1

        return poped_boards
