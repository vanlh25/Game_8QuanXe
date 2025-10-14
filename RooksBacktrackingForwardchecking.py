import random
import numpy as np

BOARD_SIZE = 8

class RooksBacktrackingForwardchecking:
    def __init__(self):
        self.tapbien = ['x0','x1','x2','x3','x4','x5','x6','x7']
        #mỗi biến ứng với một hàng, giá trị là các cột
        self.tapgiatri = {x: [(i,j) for j in range(BOARD_SIZE)] for i,x in enumerate(self.tapbien)}

    #kiểm tra ràng buộc: không được trùng cột
    def check_rangbuoc(self, arr, tuple_gtri):
        _, col = tuple_gtri
        return col not in arr

    #chuyển mảng 1D sang ma trận 8x8
    def convert_to_8x8(self, arr):
        board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        for row, col in enumerate(arr):
            if col != -1:
                board[row, col] = 1
        return board

    # backtracking + forward checking
    def backtracking(self, arr=None, bien_chuadat=None, path=None, tapgiatri=None):
        if arr is None:
            arr = [-1] * BOARD_SIZE
        if path is None:
            path = []
        if tapgiatri is None:
            tapgiatri = {x: vals.copy() for x, vals in self.tapgiatri.items()}

        path.append(arr.copy())

        if -1 not in arr:  # đã gán hết biến
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

            domain = tapgiatri[chonbien].copy()
            random.shuffle(domain)

            for row, col in domain:
                if self.check_rangbuoc(arr, (row, col)):
                    arr[row] = col

                    # forward checking
                    tapgiatri_new = {x: vals.copy() for x, vals in tapgiatri.items()}
                    for r in bien_chuachon:
                        tapgiatri_new[r] = [(rr, c) for (rr, c) in tapgiatri_new[r] if c != col]
                        if not tapgiatri_new[r]:  # nếu 1 trong số các  domain rỗng thì tức là chọn cái giá trị đó sẽ ko dẫn đến kq
                            # thì ta bỏ qua các bước tiếp theo luôn và đi đến thử giá trị tiếp theo luôn
                            break
                    else:
                        bien_conlai = bien_chuadat.copy()
                        bien_conlai.remove(chonbien)
                        result = self.backtracking(arr, bien_conlai, path, tapgiatri_new)
                        if result is not None:
                            return result
                    arr[row] = -1

        path.pop()
        return None


if __name__ == "__main__":
    bt = RooksBacktrackingForwardchecking()
    path = bt.backtracking()
    print(bt.tapbien)
    print(bt.tapgiatri)
    if path:
        print(f"Tổng số trạng thái trong đường đi: {len(path)}")
        for i, board in enumerate(path):
            print(f"\nTrạng thái {i}:\n{board}")
    else:
        print("Không tìm thấy nghiệm.")
