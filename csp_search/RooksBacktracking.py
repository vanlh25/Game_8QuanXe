import random
import time
import numpy as np

BOARD_SIZE = 8

class RooksBacktracking:
    def __init__(self):
        self.tapbien = ['x0','x1','x2','x3','x4','x5','x6','x7']
        # mỗi biến ứng với một hàng, giá trị là các cột có thể đặt
        self.tapgiatri = {x: [(i, j) for j in range(BOARD_SIZE)] for i, x in enumerate(self.tapbien)}

        # Thống kê
        self.tong_tt_dasinh = 0
        self.tong_tt_popped = 0
        self.execution_time = 0

    # kiểm tra ràng buộc: không trùng cột
    def check_rangbuoc(self, arr, tuple_gtri):
        _, col = tuple_gtri
        return col not in arr

    # chuyển arr sang ma trận 8x8
    def convert_to_8x8(self, arr):
        board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        for row, col in enumerate(arr):
            if col != -1:
                board[row, col] = 1
        return board

    # backtracking có trả về đường đi (list các trạng thái 8x8)
    def backtracking(self, arr=None, bien_chuadat=None, path=None):
        if arr is None:
            arr = [-1] * BOARD_SIZE
        if path is None:
            path = [self.convert_to_8x8(arr)]  # lưu trạng thái đầu tiên
            self.tong_tt_dasinh += 1  # tăng tổng trạng thái sinh ra

        if -1 not in arr:  # nếu gán hết → tìm thấy nghiệm
            path.append(self.convert_to_8x8(arr))
            self.tong_tt_dasinh += 1
            return path

        if bien_chuadat is None:
            bien_chuadat = self.tapbien.copy()

        if not bien_chuadat:  # không còn biến nào
            return None

        bien_chuachon = bien_chuadat.copy()

        while bien_chuachon:
            chonbien = random.choice(bien_chuachon)
            bien_chuachon.remove(chonbien)

            domain = self.tapgiatri[chonbien].copy()
            random.shuffle(domain)

            for row, col in domain:
                if self.check_rangbuoc(arr, (row, col)):
                    arr[row] = col
                    path.append(self.convert_to_8x8(arr))  # lưu mỗi bước đặt quân
                    self.tong_tt_dasinh += 1

                    bien_conlai = bien_chuadat.copy()
                    bien_conlai.remove(chonbien)

                    result = self.backtracking(arr, bien_conlai, path)
                    if result is not None:
                        return result

                    # nếu không thành công --> quay lui
                    arr[row] = -1
                    path.append(self.convert_to_8x8(arr))  # lưu lúc bỏ quân ra
                    self.tong_tt_dasinh += 1

        return None

    def run_solver(self):
        start_time = time.time()
        path = self.backtracking()
        self.execution_time = round(time.time() - start_time, 2)
        self.tong_tt_popped = len(path) if path else 0
        return path

    def thong_so(self):
        return {
            "Tổng trạng thái sinh ra": self.tong_tt_dasinh,
            "Tổng trạng thái lấy ra": self.tong_tt_popped,
            "Thời gian chạy (giây)": self.execution_time
        }


