BOARD_SIZE = 8

class RooksDLS:
    def __init__(self):
        self.initial_board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    # Kiểm tra trạng thái đích: tất cả xe nằm trên đường chéo chính
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

    # Sinh trạng thái con: đặt xe vào hàng tiếp theo
    def sinh_trang_thai_con(self, board, hang_hien_tai):
        danh_sach_con = []
        for cot in range(BOARD_SIZE):
            if all(board[h][cot] == 0 for h in range(BOARD_SIZE)):
                new_board = [row[:] for row in board]
                new_board[hang_hien_tai][cot] = 1
                danh_sach_con.append(new_board)
        return danh_sach_con

    # DLS đệ quy không dùng Node
    def DLS(self, board, hang_hien_tai, limit, popped_boards):
        # Lưu lại trạng thái đã duyệt
        popped_boards.append([row[:] for row in board])

        # Kiểm tra goal
        if self.la_trang_thai_dich(board):
            return board

        if limit == 0:
            return 'cutoff'

        cutoff_occurred = False
        children = self.sinh_trang_thai_con(board, hang_hien_tai)
        for child_board in children:
            result = self.DLS(child_board, hang_hien_tai + 1, limit - 1, popped_boards)
            if result == 'cutoff':
                cutoff_occurred = True
            elif result != 'failure':
                return result

        if cutoff_occurred:
            return 'cutoff'
        else:
            return 'failure'

    # Hàm gọi DLS từ root
    def depth_limited_search(self, limit=BOARD_SIZE):
        popped_boards = []
        result = self.DLS(self.initial_board, 0, limit, popped_boards)
        return popped_boards
