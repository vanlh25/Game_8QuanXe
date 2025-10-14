import numpy as np

BOARD_SIZE = 8
GOAL = [7, 0, 6, 2, 5, 1, 3, 4]  # vị trí quân xe trên board mục tiêu

class RooksHillClimbing:
    def __init__(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.goalboard = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        for i in range(BOARD_SIZE):
            self.goalboard[i][GOAL[i]] = 1

    def la_trang_thai_dich(self, board):
        return np.array_equal(board, self.goalboard)

    def cost_heuristic(self, board):
        """Tính số cặp quân không tấn công nhau"""
        flat = np.argmax(board, axis=1)  # vị trí cột của mỗi hàng
        N = len(flat)
        tong_cap = N * (N - 1) // 2
        tong_xe_moihang = np.bincount(flat, minlength=N)
        tong_captrung = np.sum(tong_xe_moihang * (tong_xe_moihang - 1) // 2)
        return tong_cap - tong_captrung

    def sinh_trang_thai_con(self, board, hang_hientai):
        """Sinh tất cả trạng thái con của hàng hiện tại"""
        danh_sach_con = []
        for cot in range(BOARD_SIZE):
            new_board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
            new_board[:hang_hientai] = board[:hang_hientai]  # giữ các hàng trước
            new_board[hang_hientai, cot] = 1
            chi_phi_con = self.cost_heuristic(new_board)
            danh_sach_con.append((new_board, chi_phi_con))
        return danh_sach_con

    def hill_pop_boards(self):
        """Chạy hill-climbing, luôn trả về list các board duyệt"""
        poped_boards = []
        board_hientai = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

        for hang_hientai in range(BOARD_SIZE):
            lst_children = self.sinh_trang_thai_con(board_hientai, hang_hientai)
            costs = [cost for _, cost in lst_children]
            index_maxcost = np.argmax(costs)
            best_board, best_cost = lst_children[index_maxcost]

            poped_boards.append(best_board.copy())

            current_cost = self.cost_heuristic(board_hientai)
            if best_cost <= current_cost:
                # nếu bị kẹt, vẫn trả về đường đi tới đây
                return poped_boards

            board_hientai = best_board.copy()

        return poped_boards
