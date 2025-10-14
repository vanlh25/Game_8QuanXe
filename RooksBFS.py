from collections import deque

BOARD_SIZE = 8

class RooksBFS:
    def __init__(self):
        # Bắt đầu với ma trận rỗng
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    GOAL = [0, 1, 2, 3, 6, 4, 5, 7]

    # Kiểm tra trạng thái đích: tất cả xe nằm trên đường chéo chính
    def la_trang_thai_dich(self, board):
        return (
                board[0][0] == 1 and
                board[1][1] == 1 and
                board[2][2] == 1 and
                board[3][3] == 1 and
                board[4][6] == 1 and
                board[5][4] == 1 and
                board[6][5] == 1 and
                board[7][7] == 1
        )

    # Sinh trạng thái con: đặt xe vào hàng tiếp theo
    def sinh_trang_thai_con(self, board, hang_hien_tai):
        danh_sach_con = []
        for cot in range(BOARD_SIZE):
            # Không đặt vào cột đã có xe
            if all(board[h][cot] == 0 for h in range(BOARD_SIZE)):
                new_board = [row[:] for row in board]
                new_board[hang_hien_tai][cot] = 1
                danh_sach_con.append(new_board)
        return danh_sach_con

    # BFS tìm lời giải và in từng bước
    def bfs_pop_boards(self):
        queue = deque([(self.board, 0)])  # (board, số hàng đã đặt)
        popped_boards = []
        step = 0

        while queue:
            board, hang_hien_tai = queue.popleft()


            # Lưu lại trạng thái đã lấy ra
            popped_boards.append([row[:] for row in board])

            # Nếu đã đặt đủ 8 quân thì kiểm tra đích
            if hang_hien_tai == BOARD_SIZE:
                if self.la_trang_thai_dich(board):
                    return popped_boards
                step += 1
                continue

            # Sinh trạng thái con ở hàng hiện tại
            children = self.sinh_trang_thai_con(board, hang_hien_tai)
            for child in children:
                queue.append((child, hang_hien_tai + 1))

            step += 1

        return popped_boards
