BOARD_SIZE = 8
GOAL_COLS = [7, 0, 6, 2, 5, 1, 3, 4]
class RooksGS:
    def __init__(self):
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

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

    def chi_phi(self, hang_hien_tai, cot):
        goal_col = GOAL_COLS[hang_hien_tai]
        return abs(goal_col - cot)

    def sinh_trang_thai_con(self, board, hang_hien_tai):
        danh_sach_con = []
        for cot in range(BOARD_SIZE):
            if all(board[h][cot] == 0 for h in range(BOARD_SIZE)):
                new_board = [row[:] for row in board]
                new_board[hang_hien_tai][cot] = 1
                chi_phi_con = self.chi_phi(hang_hien_tai, cot)
                danh_sach_con.append((new_board, chi_phi_con))
        return danh_sach_con

    def gs_pop_boards(self):
        from heapq import heappush, heappop

        heap = []
        heappush(heap, (0, self.board, 0))  # (chi_phi, board, hang_hien_tai)
        popped_boards = []

        while heap:
            chi_phi_hien_tai, board, hang_hien_tai = heappop(heap)
            popped_boards.append([row[:] for row in board])

            if hang_hien_tai == BOARD_SIZE:
                if self.la_trang_thai_dich(board):
                    return popped_boards
                continue

            children = self.sinh_trang_thai_con(board, hang_hien_tai)
            for child_board, chi_phi_con in children:
                heappush(heap, (chi_phi_con, child_board, hang_hien_tai + 1))

        return popped_boards
