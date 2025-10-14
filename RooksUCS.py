from heapq import heappush, heappop

BOARD_SIZE = 8

class RooksUCS:
    def __init__(self):
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.goal_positions = [7, 0, 6, 2, 5, 1, 3, 4]

    def la_trang_thai_dich(self, board):
        return all(board[i][self.goal_positions[i]] == 1 for i in range(BOARD_SIZE))

    def sinh_trang_thai_con(self, board, hang_hien_tai):
        danh_sach_con = []
        for cot in range(BOARD_SIZE):
            if all(board[h][cot] == 0 for h in range(BOARD_SIZE)):
                new_board = [row[:] for row in board]
                new_board[hang_hien_tai][cot] = 1
                chi_phi_con = 1  # mỗi lần đặt 1 quân = 1
                danh_sach_con.append((new_board, chi_phi_con))
        return danh_sach_con

    def ucs_pop_boards(self):
        heap = []
        heappush(heap, (0, self.board, 0))  # (chi_phi_tong, board, hang_hien_tai)
        popped_boards = []

        while heap:
            chi_phi_tong, board, hang_hien_tai = heappop(heap)
            popped_boards.append([row[:] for row in board])

            if hang_hien_tai == BOARD_SIZE:
                if self.la_trang_thai_dich(board):
                    return popped_boards
                continue

            children = self.sinh_trang_thai_con(board, hang_hien_tai)
            for child_board, chi_phi_con in children:
                heappush(heap, (chi_phi_tong + chi_phi_con, child_board, hang_hien_tai + 1))

        return popped_boards
