from heapq import heappush, heappop

BOARD_SIZE = 8

class RooksAS:
    def __init__(self):
        self.board = [[0]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.goal_positions = [7, 0, 6, 2, 5, 1, 3, 4]

    def la_trang_thai_dich(self, board):
        return all(board[i][self.goal_positions[i]] == 1 for i in range(BOARD_SIZE))

    def g_x(self, hang_hien_tai, cot, cot_dich):
        return abs(cot - cot_dich)

    def h_x(self, hang_hien_tai, cot):
        return abs(cot - self.goal_positions[hang_hien_tai])

    def f_x(self, g, hang_hien_tai, cot):
        return g + self.h_x(hang_hien_tai, cot)

    def sinh_trang_thai_con(self, board, hang_hien_tai):
        children = []
        for cot in range(BOARD_SIZE):
            if all(board[h][cot] == 0 for h in range(BOARD_SIZE)):
                new_board = [row[:] for row in board]
                new_board[hang_hien_tai][cot] = 1
                g = self.g_x(hang_hien_tai, cot, self.goal_positions[hang_hien_tai])
                children.append((new_board, g, cot))
        return children

    def as_pop_boards(self):
        heap = []
        heappush(heap, (0, 0, self.board, 0))
        popped_boards = []

        while heap:
            f, g, board, hang_hien_tai = heappop(heap)
            popped_boards.append([row[:] for row in board])

            if hang_hien_tai == BOARD_SIZE:
                if self.la_trang_thai_dich(board):
                    return popped_boards
                continue

            children = self.sinh_trang_thai_con(board, hang_hien_tai)
            for child_board, g_con, cot in children:
                g_new = g + g_con
                f_new = self.f_x(g_new, hang_hien_tai, cot)
                heappush(heap, (f_new, g_new, child_board, hang_hien_tai + 1))

        return popped_boards
