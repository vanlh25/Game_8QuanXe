import numpy as np
import random
import time

BOARD_SIZE = 8
GOAL = [7, 0, 6, 2, 5, 1, 3, 4]  # vị trí quân xe mục tiêu


class RooksAndOrSearch:
    def __init__(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.goalboard = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.belief = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.history = []  # lưu lịch sử để hiển thị UI

        for i, c in enumerate(GOAL):
            self.goalboard[i, c] = 1

    def random_init(self):
        # random vị trí ban đầu của các xe
        cols = list(range(BOARD_SIZE))
        random.shuffle(cols)
        for i in range(BOARD_SIZE):
            self.board[i, cols[i]] = 1

    def is_goal(self, state):
        return np.array_equal(state, self.goalboard)

    def observe(self, true_board):
        """Quan sát một phần: chỉ thấy 1 vài vị trí của goal"""
        new_belief = self.belief.copy()
        visible_rows = random.sample(range(BOARD_SIZE), k=random.randint(1, 3))
        for r in visible_rows:
            for c in range(BOARD_SIZE):
                if true_board[r, c] == 1:
                    new_belief[r, c] = 1
        return new_belief

    def actions(self, state):
        """Sinh ra các hành động hợp lệ"""
        actions = []
        for r in range(BOARD_SIZE):
            c = np.where(state[r] == 1)[0][0]
            for dc in [-1, 1]:
                nc = c + dc
                if 0 <= nc < BOARD_SIZE and state[r, nc] == 0:
                    new_state = state.copy()
                    new_state[r, c] = 0
                    new_state[r, nc] = 1
                    actions.append(new_state)
        return actions

    def and_or_search(self, state, belief):
        if self.is_goal(state):
            return [state]
        self.history.append((state.copy(), belief.copy()))
        belief = self.observe(self.goalboard)  # cập nhật belief
        actions = self.actions(state)
        for a in actions:
            result = self.and_or_search(a, belief)
            if result is not None:
                return [state] + result
        return None

    def run(self):
        self.random_init()
        print("Trạng thái khởi tạo:")
        print(self.board)
        print("\nBắt đầu tìm kiếm...\n")
        path = self.and_or_search(self.board, self.belief)

        print("Hoàn tất! Độ dài đường đi:", len(path))
        for i, (state, belief) in enumerate(self.history):
            print(f"\nBước {i}:")
            print("Trạng thái hiện tại:")
            print(state)
            print("Niềm tin (Belief):")
            print(belief)
            time.sleep(0.5)

        return path, self.history


if __name__ == "__main__":
    game = RooksAndOrSearch()
    path, history = game.run()
