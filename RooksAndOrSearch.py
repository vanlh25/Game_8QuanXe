import numpy as np

BOARD_SIZE = 8
GOAL = [7,0,6,2,5,1,3,4]  # vị trí quân xe trên board mục tiêu

class RooksAndOrSearch:
    def __init__(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.goalboard = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        for i in range(BOARD_SIZE):
            self.goalboard[i][GOAL[i]] = 1

    def la_trang_thai_dich(self, board):
        return np.array_equal(board, self.goalboard)

    def hanhdongs(self, board):
        hanhdongs = []
        n_rooks = int(np.sum(board))
        if n_rooks < BOARD_SIZE:
            # Chỉ đặt ở hàng tiếp theo (để tránh trùng)
            row = n_rooks
            for col in range(BOARD_SIZE):
                # cột đó chưa có quân nào
                if np.all(board[:, col] == 0):
                    hanhdongs.append(("dat", row, col))
        else:
            # Di chuyển khi đã đủ quân
            for row in range(BOARD_SIZE):
                col = np.where(board[row] == 1)[0][0]
                goal_col = GOAL[row]
                if col < goal_col and col + 1 < BOARD_SIZE:
                    hanhdongs.append(("move", row, col, "right"))
                elif col > goal_col and col - 1 >= 0:
                    hanhdongs.append(("move", row, col, "left"))
        return hanhdongs

    def results(self, board, hanhdong):
        loai = hanhdong[0]
        list_tt_moi = []

        if loai == "dat":
            _, row, col = hanhdong
            new_board = board.copy()
            new_board[row, col] = 1
            list_tt_moi.append(new_board)

        elif loai == "move":
            _, row, col, huong = hanhdong
            new_board = board.copy()
            new_board[row, col] = 0
            if huong == "left":
                new_board[row, col - 1] = 1
            else:
                new_board[row, col + 1] = 1
            list_tt_moi.append(new_board)

        return list_tt_moi

    def and_or_search(self):
        plan = self.or_search(self.board, [])
        if plan:
            print("Tìm thấy kế hoạch!")
        else:
            print("Không tìm thấy kế hoạch.")
        return plan

    def or_search(self, state, path):
        if self.la_trang_thai_dich(state):
            return [state]

        if any(np.array_equal(state, p) for p in path):
            return None

        for action in self.hanhdongs(state):
            results = self.results(state, action)
            subplan = self.and_search(results, path + [state])
            if subplan is not None:
                return [state] + subplan
        return None

    def and_search(self, states, path):
        plan = []
        for s in states:
            subplan = self.or_search(s, path)
            if subplan is None:
                return None
            plan.extend(subplan)
        return plan


# ---- MAIN TEST ----
if __name__ == "__main__":
    solver = RooksAndOrSearch()
    plan = solver.and_or_search()
    if plan:
        print(f"\nTìm được kế hoạch gồm {len(plan)} bước:\n")
        for i, board in enumerate(plan):
            print(f"Bước {i+1}:")
            print(board)
    else:
        print("Không tìm được kế hoạch.")
