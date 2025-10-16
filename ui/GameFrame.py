# GameFrame.py
import pygame
import pygame.freetype
import numpy as np
from collections import deque
import time

from complex_env_search.RookPartial import RooksPartial
# Import các thuật toán
from complex_env_search.RooksAndOrSearch import RooksAndOrSearch
from csp_search.RooksBacktracking import RooksBacktracking
from csp_search.RooksBacktrackingAC3 import RooksBacktrackingAC3
from csp_search.RooksBacktrackingForwardchecking import RooksBacktrackingForwardchecking
from local_search.RooksBeamSearch import RooksBeamSearch
from complex_env_search.RooksBelief import RooksBelief
from local_search.RooksGenetic import RooksGenetic
from informed_search.RooksAS import RooksAS
from uninformed_search.RooksBFS import RooksBFS
from uninformed_search.RooksDFS import RooksDFS
from uninformed_search.RooksDLS import RooksDLS
from informed_search.RooksGS import RooksGS
from local_search.RooksHillClimbing import RooksHillClimbing
from uninformed_search.RooksIDS import RooksIDS
from local_search.RooksSimulatedAnnealing import RooksSimulatedAnnealing
from uninformed_search.RooksUCS import RooksUCS

BOARD_SIZE = 8
CELL = 45          # kích thước mỗi ô
BOARD_GAP = 40     # khoảng cách giữa 2 bàn
GOAL = [7, 0, 6, 2, 5, 1, 3, 4] # vị trí quân xe trên board mục tiêu

class GameFrame:
    def __init__(self, app):
        self.app = app
        self.font = pygame.freetype.SysFont("Times New Roman", 50, bold=True)
        self.font_rook = pygame.freetype.SysFont("Segoe UI Symbol", 40, bold=True)
        # Hai board
        self.left_board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.right_board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        for i in range(BOARD_SIZE):
            self.right_board[i][GOAL[i]] = 1

        self.current_algorithm_name = ""

        # Nút
        self.solve_button = pygame.Rect(100, 450, 70, 40)
        self.back_button = pygame.Rect(200,450, 70, 40)
        self.reset_button = pygame.Rect(300, 450, 70, 40)
        self.dropdown = pygame.Rect(400, 450, 200, 40)
        self.pause_button = pygame.Rect(650, 450, 70, 40)
        self.stats_button = pygame.Rect(750, 450, 120, 40)  # nút bật/tắt thống kê

        self.paused = False
        self.stats_visible = False

        # Dropdown thuật toán
        self.algorithms = [
            "BFS Search", "DFS Search", "UCS Search", "DLS Search", "IDS Search", "GS Search", "AS Search", "Hill Search", "Simulated Annealing","Beam Search", "Genetic Search",
            "And Or Search","Belief Search","Partial Search","Backtracking Search", "Forward checking Search","AC-3 Search"
        ]
        self.selected_algo = self.algorithms[0]
        self.show_dropdown = False
        self.dropdown_offset = 0
        self.dropdown_max_visible = 4
        self.dropdown_item_height = 40

        # Vị trí bàn
        self.left_board_pos = (35, 50)
        self.right_board_pos = (self.left_board_pos[0] + CELL*BOARD_SIZE + BOARD_GAP, 50)

        # Vùng hiển thị thống kê
        self.stats_pos = (self.right_board_pos[0] + CELL*BOARD_SIZE + 20, self.right_board_pos[1])
        self.stats_line_height = 30

        # Animation
        self.animation_list = []
        self.animation_index = 0
        self.animation_delay = 60
        self.last_update = 0
        self.animating = False

        self.current_solver_obj = None  # lưu object thuật toán hiện tại

        # Vùng hiển thị thống kê
        self.stats_pos = (self.right_board_pos[0] + CELL * BOARD_SIZE + 50, self.right_board_pos[1])
        self.stats_width = 320  # chiều rộng khung thông số
        self.stats_height = 200  # chiều cao khung (tùy chỉnh)
        self.stats_line_height = 25


    # -------------------- SỰ KIỆN --------------------
    def handle_events(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                self.app.running = False

            if e.type == pygame.MOUSEWHEEL and self.show_dropdown:
                self.dropdown_offset -= e.y*4
                max_offset = max(0, len(self.algorithms) - self.dropdown_max_visible)
                self.dropdown_offset = min(max(self.dropdown_offset, 0), max_offset)

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self.solve_button.collidepoint(e.pos):
                    self.click_solve()
                elif self.back_button.collidepoint(e.pos):
                    self.click_back()
                elif self.reset_button.collidepoint(e.pos):
                    self.click_reset()
                elif self.dropdown.collidepoint(e.pos):
                    self.toggle_dropdown()
                elif self.pause_button.collidepoint(e.pos):
                    self.paused = not self.paused
                elif self.stats_button.collidepoint(e.pos):
                    self.stats_visible = not self.stats_visible
                elif self.show_dropdown:
                    start = self.dropdown_offset
                    end = min(start + self.dropdown_max_visible, len(self.algorithms))
                    for idx, i in enumerate(range(start, end)):
                        rect = pygame.Rect(self.dropdown.x, self.dropdown.y - (idx+1)*self.dropdown_item_height,
                                           self.dropdown.width, self.dropdown_item_height)
                        if rect.collidepoint(e.pos):
                            self.select_algorithm(i)
                            break

    # -------------------- VẼ BÀN CỜ --------------------
    def draw_board(self, board, x0, y0, title=""):
        self.font.render_to(self.app.screen, (x0+30 , y0 - 30), title, (139, 69, 19), size=20)
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                color = (240, 217, 181) if (i + j) % 2 == 0 else (181, 136, 99)
                rect = pygame.Rect(x0 + j * CELL, y0 + i * CELL, CELL, CELL)
                pygame.draw.rect(self.app.screen, color, rect)
                pygame.draw.rect(self.app.screen, (200,200,200), rect,2)
                pygame.draw.rect(self.app.screen, (50,50,50), rect,1)
                if board[i][j] == 1:
                    char_surf, char_rect = self.font_rook.render("♜", (0,0,0), size=40)
                    char_rect.center = rect.center
                    self.app.screen.blit(char_surf, char_rect)

    # -------------------- DROPDOWN --------------------
    def draw_dropdown(self):
        if self.show_dropdown:
            start = self.dropdown_offset
            end = min(start + self.dropdown_max_visible, len(self.algorithms))
            for idx, i in enumerate(range(start, end)):
                rect = pygame.Rect(self.dropdown.x, self.dropdown.y - (idx+1)*self.dropdown_item_height,
                                   self.dropdown.width, self.dropdown_item_height)
                pygame.draw.rect(self.app.screen, (240,240,240), rect, border_radius=5)
                pygame.draw.rect(self.app.screen, (0,0,0), rect, 1, border_radius=5)
                txt_surf, txt_rect = self.font.render(self.algorithms[i], (0,0,0), size=18)
                txt_rect.center = rect.center
                self.app.screen.blit(txt_surf, txt_rect)

    # -------------------- VẼ THỐNG KÊ --------------------
    def draw_stats(self):
        if self.current_solver_obj is None:
            return

        # Vẽ khung nền trắng
        pygame.draw.rect(
            self.app.screen,
            (255, 255, 255),
            (self.stats_pos[0] - 10, self.stats_pos[1] - 10, self.stats_width, self.stats_height),
            border_radius=10
        )
        pygame.draw.rect(
            self.app.screen,
            (0, 0, 0),
            (self.stats_pos[0] - 10, self.stats_pos[1] - 10, self.stats_width, self.stats_height),
            3,
            border_radius=10
        )

        x, y = self.stats_pos

        # Vẽ tên thuật toán to hơn
        txt_surf, txt_rect = self.font.render(f"Algorithm: {self.current_algorithm_name}", (0, 0, 0), size=20)
        txt_rect.topleft = (x, y)
        self.app.screen.blit(txt_surf, txt_rect)

        # Vẽ thông số bên dưới tên thuật toán
        stats = self.current_solver_obj.thong_so()
        for i, (key, value) in enumerate(stats.items()):
            txt_surf, txt_rect = self.font.render(f"{key}: {value}", (0, 0, 0), size=18)
            txt_rect.topleft = (x, y + (i + 1) * self.stats_line_height)
            self.app.screen.blit(txt_surf, txt_rect)

    # -------------------- VẼ TỔNG QUÁT --------------------
    def draw(self):
        self.app.screen.fill((152,251,152))  # nền xanh nhẹ
        self.draw_board(self.left_board, *self.left_board_pos, "Left Board")
        self.draw_board(self.right_board, *self.right_board_pos, "Right Board (GOAL)")

        # Nút Solve
        pygame.draw.rect(self.app.screen, (255,255,255), self.solve_button, border_radius=10)
        pygame.draw.rect(self.app.screen, (0,0,0), self.solve_button, 2, border_radius=10)
        txt_surf, txt_rect = self.font.render("Solve", (0,0,0), size=20)
        txt_rect.center = self.solve_button.center
        self.app.screen.blit(txt_surf, txt_rect)

        # Nút Back
        pygame.draw.rect(self.app.screen, (255,255,255), self.back_button, border_radius=10)
        pygame.draw.rect(self.app.screen, (0,0,0), self.back_button, 2, border_radius=10)
        txt_surf, txt_rect = self.font.render("Back", (0,0,0), size=20)
        txt_rect.center = self.back_button.center
        self.app.screen.blit(txt_surf, txt_rect)

        # Nút Pause/Resume
        pygame.draw.rect(self.app.screen, (255,255,255), self.pause_button, border_radius=10)
        pygame.draw.rect(self.app.screen, (0,0,0), self.pause_button, 2, border_radius=10)
        txt = "Resume" if self.paused else "Pause"
        txt_surf, txt_rect = self.font.render(txt, (0,0,0), size=20)
        txt_rect.center = self.pause_button.center
        self.app.screen.blit(txt_surf, txt_rect)

        # Nút Reset
        pygame.draw.rect(self.app.screen, (255,255,255), self.reset_button, border_radius=10)
        pygame.draw.rect(self.app.screen, (0,0,0), self.reset_button, 2, border_radius=10)
        txt_surf, txt_rect = self.font.render("Reset", (0,0,0), size=20)
        txt_rect.center = self.reset_button.center
        self.app.screen.blit(txt_surf, txt_rect)

        # Dropdown thuật toán
        pygame.draw.rect(self.app.screen, (211,211,211), self.dropdown, border_radius=10)
        pygame.draw.rect(self.app.screen, (0,0,0), self.dropdown, 2, border_radius=10)
        txt_surf, txt_rect = self.font.render("Choice Algorithm", (0,0,0), size=20)
        txt_rect.center = self.dropdown.center
        self.app.screen.blit(txt_surf, txt_rect)
        self.draw_dropdown()

        # Nút Stats
        pygame.draw.rect(self.app.screen, (255,255,255), self.stats_button, border_radius=10)
        pygame.draw.rect(self.app.screen, (0,0,0), self.stats_button, 2, border_radius=10)
        txt_surf, txt_rect = self.font.render("Stats", (0,0,0), size=20)
        txt_rect.center = self.stats_button.center
        self.app.screen.blit(txt_surf, txt_rect)

        # Animation và Stats
        self.update_animation()
        if self.stats_visible:
            self.draw_stats()

    # -------------------- GIẢI THUẬT TOÁN --------------------
    def start_solver(self):
        self.reset_board()
        self.run_classic_solver(self.selected_algo)

    def run_classic_solver(self, algo_name):
        solvers = {
            "BFS Search": (RooksBFS, "bfs_pop_boards"),
            "DFS Search": (RooksDFS, "dfs_pop_boards"),
            "UCS Search": (RooksUCS, "ucs_pop_boards"),
            "DLS Search": (RooksDLS, "depth_limited_search"),
            "IDS Search": (RooksIDS, "ids_pop_boards"),
            "GS Search": (RooksGS, "gs_pop_boards"),
            "AS Search": (RooksAS, "as_pop_boards"),
            "Genetic Search": (RooksGenetic, "genetic_run"),
            "Hill Search": (RooksHillClimbing, "hill_pop_boards"),
            "Simulated Annealing": (RooksSimulatedAnnealing, "simulatedAnnealing_pop_boards"),
            "Beam Search": (RooksBeamSearch, "beamSearch_pop_boards"),
            "And Or Search": (RooksAndOrSearch, "and_or_search"),
            "Belief Search": (RooksBelief, "belief_search"),
            "Partial Search": (RooksPartial, "partial_search"),
            "Backtracking Search": (RooksBacktracking, "backtracking"),
            "Forward checking Search": (RooksBacktrackingForwardchecking, "backtracking"),
            "AC-3 Search": (RooksBacktrackingAC3, "backtracking"),
        }

        if algo_name not in solvers:
            self.animating = False
            msg_surf, msg_rect = self.font.render(f"Algorithm {algo_name} not found!", (255,0,0), size=30)
            msg_rect.center = (self.app.screen.get_width()//2, self.app.screen.get_height()//2)
            self.app.screen.blit(msg_surf, msg_rect)
            pygame.display.flip()
            pygame.time.delay(200)
            return

        solver_class, method_name = solvers[algo_name]
        solver = solver_class()
        self.current_solver_obj = solver
        self.current_algorithm_name = algo_name
        result = getattr(solver, method_name)()

        if result is None:
            self.animating = False
            msg_surf, msg_rect = self.font.render("No result", (255,0,0), size=30)
            msg_rect.center = (self.app.screen.get_width()//2, self.app.screen.get_height()//2)
            self.app.screen.blit(msg_surf, msg_rect)
            pygame.display.flip()
            pygame.time.delay(200)
            return

        self.animation_list = result
        self.animation_index = 0
        self.last_update = pygame.time.get_ticks()
        self.animating = True

    # -------------------- ANIMATION --------------------
    def update_animation(self):
        if self.animating and not self.paused and self.animation_list:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.animation_delay:
                self.left_board = [row[:] for row in self.animation_list[self.animation_index]]
                self.animation_index += 1
                self.last_update = now
                if self.animation_index >= len(self.animation_list):
                    self.animating = False

    def reset_board(self):
        self.animating = False
        self.left_board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

    # -------------------- NÚT --------------------
    def click_solve(self):
        self.start_solver()

    def click_back(self):
        self.app.state = "MENU"
        self.app.game_frame = None

    def click_reset(self):
        self.animating = False
        self.left_board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

    def toggle_dropdown(self):
        self.show_dropdown = not self.show_dropdown

    def select_algorithm(self, algo_index):
        if 0 <= algo_index < len(self.algorithms):
            self.selected_algo = self.algorithms[algo_index]
            self.start_solver()
        self.show_dropdown = False
