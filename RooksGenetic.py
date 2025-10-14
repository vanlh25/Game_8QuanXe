import itertools
import numpy as np
import random

BOARD_SIZE = 8
GOAL = [7,0,6,2,5,1,3,4]

class RooksGenetic:
    def __init__(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.goalboard = np.zeros((BOARD_SIZE,BOARD_SIZE), dtype=int)
        for i in range(BOARD_SIZE):
            self.goalboard[i][GOAL[i]] = 1

        self.population_size = 16
        self.mutation_rate = 0.1
        self.max_generations = 100

    def la_trang_thai_dich(self, flat):
        board = self.Chuyen_1Dsang2D(flat)
        return np.array_equal(board, self.goalboard)

    def Tao_Cathe_Bandau(self):
        return np.random.permutation(BOARD_SIZE)

    def fitness(self, flat):
        # Số lượng vị trí cột khác nhau càng nhiều thì fitness càng cao
        return len(set(flat))

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
        population = [self.Tao_Cathe_Bandau() for _ in range(self.population_size)]
        poped_board = [self.Chuyen_1Dsang2D(c) for c in population]

        for generation in range(self.max_generations):
            for cathe in population:
                if self.la_trang_thai_dich(cathe):
                    return poped_board  # Trả danh sách trạng thái duyệt

            lst_chame = self.Tinh_fitness_chame(population)
            top_pairs = lst_chame[:self.population_size]
            new_population = []
            for (p1, p2), _ in top_pairs:
                child = self.Lai(p1, p2)
                child = self.Dotbien(child)
                new_population.append(child)

            population = new_population
            poped_board.extend([self.Chuyen_1Dsang2D(c) for c in population])

        return poped_board
