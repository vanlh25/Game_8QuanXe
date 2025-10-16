import itertools
import numpy as np
import random
import time

BOARD_SIZE = 8
GOAL = [7,0,6,2,5,1,3,4]

class RooksGenetic:
    def __init__(self, population_size=16, mutation_rate=0.1, max_generations=100):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.goalboard = np.zeros((BOARD_SIZE,BOARD_SIZE), dtype=int)
        for i in range(BOARD_SIZE):
            self.goalboard[i][GOAL[i]] = 1

        # Thông số GA
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations

        # Thống kê
        self.find_goal = False
        self.tong_tt_dasinh = 0
        self.tong_tt_popped = 0
        self.tong_sobuoc = 0
        self.execution_time = 0

        # Trạng thái cuối cùng
        self.board_cuoi = None

    def la_trang_thai_dich(self, flat):
        board = self.Chuyen_1Dsang2D(flat)
        return np.array_equal(board, self.goalboard)

    def Tao_Cathe_Bandau(self):
        return np.random.permutation(BOARD_SIZE)

    def fitness(self, flat):
        return len(set(flat))  # số lượng cột khác nhau càng nhiều càng tốt

    def Tinh_fitness_chame(self, population):
        all_pairs = list(itertools.combinations(population, 2))
        lst_chame = []
        for p1, p2 in all_pairs:
            tong_fitness = self.fitness(p1) + self.fitness(p2)
            lst_chame.append(((p1, p2), tong_fitness))
        lst_chame.sort(key=lambda x: x[1], reverse=True)
        return lst_chame

    def Lai(self, cha, me):
        n = len(cha)
        mid = n // 2
        child1 = np.concatenate((cha[:mid], me[mid:]))
        child2 = np.concatenate((me[:mid], cha[mid:]))
        return child1 if self.fitness(child1) >= self.fitness(child2) else child2

    def Dotbien(self, cathe):
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(BOARD_SIZE), 2)
            cathe[i], cathe[j] = cathe[j], cathe[i]
        return cathe

    def Chuyen_1Dsang2D(self, flat):
        board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        for i, col in enumerate(flat):
            board[i, col] = 1
        return board

    def genetic_run(self):
        start_time = time.time()
        population = [self.Tao_Cathe_Bandau() for _ in range(self.population_size)]
        poped_boards = [self.Chuyen_1Dsang2D(c) for c in population]
        self.tong_tt_dasinh = len(population)
        self.tong_tt_popped = len(poped_boards)
        self.tong_sobuoc = 0

        for generation in range(self.max_generations):
            for cathe in population:
                if self.la_trang_thai_dich(cathe):
                    self.find_goal = True
                    self.board_cuoi = self.Chuyen_1Dsang2D(cathe)
                    self.execution_time = round(time.time() - start_time, 2)
                    return poped_boards

            lst_chame = self.Tinh_fitness_chame(population)
            top_pairs = lst_chame[:self.population_size]
            new_population = []
            for (p1, p2), _ in top_pairs:
                child = self.Lai(p1, p2)
                child = self.Dotbien(child)
                new_population.append(child)

            population = new_population
            poped_boards.extend([self.Chuyen_1Dsang2D(c) for c in population])
            self.tong_tt_dasinh += len(population)
            self.tong_tt_popped += len(population)
            self.tong_sobuoc += 1

        self.board_cuoi = self.Chuyen_1Dsang2D(population[0])
        self.execution_time = round(time.time() - start_time, 2)
        return poped_boards

    def thong_so(self):
        ghi_chu = ""
        if self.board_cuoi is not None:
            # Kiểm tra hợp lệ: mỗi hàng và mỗi cột chỉ có 1 quân
            row_ok = all(sum(self.board_cuoi[i]) == 1 for i in range(BOARD_SIZE))
            col_ok = all(sum(self.board_cuoi[:, j]) == 1 for j in range(BOARD_SIZE))
            khac_goal = not np.array_equal(self.board_cuoi, self.goalboard)

            if row_ok and col_ok and khac_goal:
                ghi_chu = "Bàn cờ cuối thỏa ĐK 8 quân xe!"

        return {
            "Tìm được lời giải": self.find_goal,
            "Tổng trạng thái sinh ra": self.tong_tt_dasinh,
            "Tổng trạng thái lấy ra": self.tong_tt_popped,
            "Số thế hệ chạy": self.tong_sobuoc,
            "Thời gian chạy (giây)": self.execution_time,
            "Note": ghi_chu
        }
