import numpy as np
import time

BOARD_SIZE = 8
GOAL = [7,0,6,2,5,1,3,4]  # vị trí quân xe trên board mục tiêu

class RooksAndOrSearch:
    def __init__(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.goalboard = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        for i in range(BOARD_SIZE):
            self.goalboard[i][GOAL[i]] = 1

        # Thống kê
        self.tong_tt_dasinh = 0
        self.tong_tt_popped = 0
        self.execution_time = 0
        self.board_cuoi = None
        self.find_goal = False

    def la_trang_thai_dich(self, board):
        return np.array_equal(board, self.goalboard)

    def hanhdongs(self, board):
        hanhdongs = []
        n_rooks = int(np.sum(board))
        if n_rooks < BOARD_SIZE:
            row = n_rooks
            for col in range(BOARD_SIZE):
                if np.all(board[:, col] == 0):
                    hanhdongs.append(("dat", row, col))
        else:
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
        self.tong_tt_dasinh += len(list_tt_moi)
        return list_tt_moi

    def and_or_search(self):
        start_time = time.time()
        plan = self.or_search(self.board, [])
        self.execution_time = round(time.time() - start_time, 2)
        if plan:
            self.find_goal = True
            self.board_cuoi = plan[-1]
        elif plan is None:
            self.board_cuoi = None
        return plan

    def or_search(self, state, path):
        self.tong_tt_popped += 1
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
            "Thời gian chạy (giây)": self.execution_time,
            "Note": ghi_chu
        }

# ---- MAIN TEST ----
if __name__ == "__main__":
    solver = RooksAndOrSearch()
    plan = solver.and_or_search()
    if plan:
        print(f"Tìm được kế hoạch gồm {len(plan)} bước")
    else:
        print("Không tìm được kế hoạch")
    print(solver.thong_so())
