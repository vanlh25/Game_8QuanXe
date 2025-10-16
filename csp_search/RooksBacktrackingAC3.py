import random
import time
import numpy as np
from collections import deque

BOARD_SIZE = 8

class RooksBacktrackingAC3:
    def __init__(self):
        self.tapbien = ['x0','x1','x2','x3','x4','x5','x6','x7']
        self.tapgiatri = {x: [(i,j) for j in range(BOARD_SIZE)] for i,x in enumerate(self.tapbien)}

        # Thống kê
        self.tong_tt_dasinh = 0
        self.tong_tt_popped = 0
        self.execution_time = 0

    def check_rangbuoc(self, arr, tuple_gtri):
        _, col = tuple_gtri
        return col not in arr

    def convert_to_8x8(self, arr):
        board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        for row, col in enumerate(arr):
            if col != -1:
                board[row, col] = 1
        return board

    def ac3(self, domains, constraints):
        queue = deque(constraints)
        while queue:
            (xi, xj) = queue.popleft()
            if self.revise(domains, xi, xj):
                if not domains[xi]:
                    return False
                for xk in domains.keys():
                    if xk != xi and xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(self, domains, xi, xj):
        revised = False
        to_remove = []
        for (ri, ci) in domains[xi]:
            if not any(ci != cj for (rj, cj) in domains[xj]):
                to_remove.append((ri, ci))
        for v in to_remove:
            domains[xi].remove(v)
            revised = True
        return revised

    def backtracking(self, arr=None, bien_chuadat=None, path=None, domains=None):
        if arr is None:
            arr = [-1]*BOARD_SIZE
        if path is None:
            path = []
        if domains is None:
            domains = {x: vals.copy() for x, vals in self.tapgiatri.items()}

        # trạng thái sinh ra
        self.tong_tt_dasinh += 1
        path.append(arr.copy())

        if -1 not in arr:  # đã gán hết
            self.tong_tt_popped = len(path)
            return [self.convert_to_8x8(a) for a in path]

        if bien_chuadat is None:
            bien_chuadat = self.tapbien.copy()

        if not bien_chuadat:
            path.pop()
            return None

        bien_chuachon = bien_chuadat.copy()

        while bien_chuachon:
            chonbien = random.choice(bien_chuachon)
            bien_chuachon.remove(chonbien)
            domain = domains[chonbien].copy()
            random.shuffle(domain)

            for row, col in domain:
                if self.check_rangbuoc(arr, (row, col)):
                    arr[row] = col

                    new_domains = {x: vals.copy() for x, vals in domains.items()}
                    new_domains[chonbien] = [(row, col)]
                    constraints = [(xi, xj) for xi in new_domains for xj in new_domains if xi != xj]

                    if self.ac3(new_domains, constraints):
                        bien_conlai = bien_chuadat.copy()
                        bien_conlai.remove(chonbien)
                        result = self.backtracking(arr, bien_conlai, path, new_domains)
                        if result is not None:
                            return result
                    arr[row] = -1  # quay lui

        path.pop()
        return None

    def run_solver(self):
        start_time = time.time()
        path = self.backtracking()
        self.execution_time = round(time.time() - start_time, 2)
        return path

    def thong_so(self):
        return {
            "Tổng trạng thái sinh ra": self.tong_tt_dasinh,
            "Tổng trạng thái lấy ra": self.tong_tt_popped,
            "Thời gian chạy (giây)": self.execution_time
        }


if __name__ == "__main__":
    r = RooksBacktrackingAC3()
    path = r.run_solver()

    if path:
        print(f"Tổng số trạng thái trong đường đi: {len(path)}")
        for i, board in enumerate(path):
            print(f"\nTrạng thái {i}:\n{board}")
    else:
        print("Không tìm thấy nghiệm.")

    print("\n=== Thống kê ===")
    print(r.thong_so())
