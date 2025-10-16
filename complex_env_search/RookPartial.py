import random
import time

import numpy as np

BOARD_SIZE = 8
SIZE_INITS = 3
SIZE_GOALS = 32000

"""
Tu ma tran 8x8 ta chuyen ve ma tran 1D voi 8 phan tu
Co the chuyen duoc nhu the boi vi ta quy uoc moi hang chi dat mot quan xe
Index --> vi tri hang
Gia tri ---> Vi tri cot 
"""

class RooksPartial:
    def __init__(self):
        random.seed(42)
        # Partial goal cố định
        self.partial_goal = [(0, 1), (1, 3), (2, 5)]
        # List goal: mỗi goal đều thỏa partial goal
        self.list_goals = []
        self.khoitao_goals()

        self.list_inits = [] # list cac trang thai init (np.array)
        self.khoitao_inits()

        self.set_visited = set() # luu cac state da di qua
        # Thống kê
        self.tong_tt_dasinh = 0
        self.tong_tt_popped = 0
        self.execution_time = 0

    def khoitao_goals(self):
        for i in range(SIZE_GOALS):
            tmp = tuple(random.sample(range(0, 8), 8))
            self.list_goals.append(tmp)
        self.list_goals.append((0,1,2,3,4,5,6,7))

    def check_partial_goal(self, arr):
        for row, col in self.partial_goal:
            if arr[row] != col:
                return False
        return True

    def khoitao_inits(self):
        arr_rong = np.array([1, 0, 2, 3, 7, -1, -1, -1])
        arr_gtri = np.array([5, -1, 2, 6, 4, 1, 3, -1])
        arr_full = np.array([0, 1, 2, 2, 3, 4, 6, 7])
        self.list_inits.extend([arr_rong, arr_full, arr_gtri])

    # Kiem tra xem da di qua chua
    def check_visited(self, list_arr):
        tuple_arr = tuple(tuple(x) for x in list_arr)
        if tuple_arr in self.set_visited:
            return True
        self.set_visited.add(tuple_arr)
        return False

    # Kiem tra 1 arr co phai goal khong
    def check_is_goal(self, arr):
        return tuple(arr) in self.list_goals

    # Kiem tra tat ca arr trong list_arr co phai goal khong
    def check_is_listgoals(self, list_arr):
        return all(tuple(arr) in self.list_goals for arr in list_arr)

    # Sinh cac trang thai con
    def sinhtrangthaicon(self, list_arr):
        list_dat = []
        list_move = []

        for arr in list_arr:
            # Nếu thỏa partial goal -> không sinh con
            if self.check_partial_goal(arr):
                list_dat.append(arr.copy())
                list_move.append(arr.copy())
                continue

            # Đặt quân xe nếu arr là goal
            if self.check_is_goal(arr):
                list_dat.append(arr.copy())
                list_move.append(arr.copy())
                continue

            count = np.sum(arr == -1)
            # Nếu còn phần tử -1 -> thay bằng số còn thiếu
            if count > 0:
                list_move.append(arr.copy())
                idx = np.argmax(arr == -1)  # vị trí đầu tiên của -1
                missing = np.setdiff1d(np.arange(8), arr[arr != -1])[0]  # số còn thiếu
                arr[idx] = missing
                list_dat.append(arr.copy())
                continue

            # Nếu không còn -1, kiểm tra phần tử trùng
            if count == 0:
                list_dat.append(arr.copy())
                seen = set()
                dup_idx = None
                for i, val in enumerate(arr):
                    if val in seen:
                        dup_idx = i
                        break
                    seen.add(val)

                if dup_idx is not None:
                    dup_val = arr[dup_idx]
                    missing = np.setdiff1d(np.arange(8), arr)[0]  # số còn thiếu
                    # di chuyển phần tử trùng về hướng số còn thiếu
                    if missing > dup_val:
                        arr[dup_idx] += 1
                    else:
                        arr[dup_idx] -= 1
                list_move.append(arr.copy())

        return list_move, list_dat

    def convert_to_8x8_boards(self, list_arr):
        boards = []
        for arr in list_arr:
            board = np.zeros((8, 8), dtype=int)
            for row, col in enumerate(arr):
                if col != -1:  # nếu đã đặt quân
                    board[row, col] = 1
            boards.append(board)
        return boards

    def partial_search(self):
        start_time = time.time()

        stack_cac_trangthai = [self.list_inits.copy()]
        self.check_visited(self.list_inits.copy())

        history_8x8 = []
        while stack_cac_trangthai:
            list_arr = stack_cac_trangthai.pop()
            self.tong_tt_popped+=1
            board8 = self.convert_to_8x8_boards(list_arr)
            history_8x8.extend(board8)
            if self.check_is_listgoals(list_arr):
                self.execution_time = round(time.time() - start_time, 2)
                return history_8x8
            for list_arr_sinh in self.sinhtrangthaicon(list_arr):
                if not self.check_visited(list_arr_sinh):
                    stack_cac_trangthai.append(list_arr_sinh)
                    self.tong_tt_dasinh+=1
        self.execution_time = round(time.time() - start_time, 2)
        return None

    def thong_so(self):
        return {
            "Tổng các bộ trạng thái sinh ra": self.tong_tt_dasinh,
            "Tổng các bộ trạng thái lấy ra": self.tong_tt_popped,
            "Thời gian chạy (giây)": getattr(self, 'execution_time', None),
        }



