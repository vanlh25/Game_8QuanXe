# GameFrame.py
import pygame
import numpy as np

from RooksAndOrSearch import RooksAndOrSearch
from RooksBacktracking import RooksBacktracking
from RooksBacktrackingAC3 import RooksBacktrackingAC3
from RooksBacktrackingForwardchecking import RooksBacktrackingForwardchecking
from RooksBeamSearch import RooksBeamSearch
from RooksBelief import RooksBelief
from RooksGenetic import RooksGenetic
from RooksAS import RooksAS
from RooksBFS import RooksBFS
from RooksDFS import RooksDFS
from RooksDLS import RooksDLS
from RooksGS import RooksGS
from RooksHillClimbing import RooksHillClimbing
from RooksIDS import RooksIDS
from RooksSimulatedAnnealing import RooksSimulatedAnnealing
from RooksUCS import RooksUCS

BOARD_SIZE = 8
CELL = 60          # kích thước mỗi ô
BOARD_GAP = 50     # khoảng cách giữa 2 bàn
GOAL = [7, 0, 6, 2, 5, 1, 3, 4] # vị trí quân xe trên board mục tiêu

class GameFrame:
    def __init__(self, app):
        self.app = app
        self.font = pygame.freetype.SysFont("Segoe UI Symbol", 50, bold=True)

        # Hai board
        self.left_board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.right_board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        for i in range(BOARD_SIZE):
            self.right_board[i][GOAL[i]] = 1

        # Nút
        self.solve_button = pygame.Rect(100, 550, 70, 40)
        self.back_button = pygame.Rect(200, 550, 70, 40)
        self.reset_button = pygame.Rect(300, 550, 70, 40)
        self.dropdown = pygame.Rect(400, 550, 200, 40)
        self.paused = False  # mặc định không pause
        self.pause_button = pygame.Rect(600, 550, 70, 40)  # nút Pause/Resume

        # Dropdown thuật toán
        self.algorithms = [
            "BFS", "DFS", "UCS", "DLS", "IDS", "GS", "AS", "Genetic", "Hill", "simulatedAnnealing","beamSearch","AndOrSearch","Belief","Backtracking", "BTFC","AC-3"
        ]
        self.selected_algo = self.algorithms[0]  #Chọn thuật toán mặc định là thuật toán đầu tiên
        self.show_dropdown = False  #tắt show dropdown
        self.dropdown_offset = 0 #Bắt đầu từ 0
        self.dropdown_max_visible = 4 #tối đa có 4 item
        self.dropdown_item_height = 40 #chiều cao mỗi mục là 40px

        # Vị trí bàn
        self.left_board_pos = (35, 50)
        self.right_board_pos = (self.left_board_pos[0] + CELL*BOARD_SIZE + BOARD_GAP, 50)

        # Animation - cập nhật bàn cờ
        self.animation_list = []
        self.animation_index = 0
        self.animation_delay = 300  # ms
        self.last_update = 0
        self.animating = False

    # Xử lý sự kiện
    def handle_events(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                self.app.running = False

            # Scroll chuột khi dropdown mở
            if e.type == pygame.MOUSEWHEEL and self.show_dropdown:
                self.dropdown_offset -= e.y*4  # mỗi lần cuộn, nhảy 4 item
                max_offset = max(0, len(self.algorithms) - self.dropdown_max_visible)
                if self.dropdown_offset < 0:
                    self.dropdown_offset = 0
                elif self.dropdown_offset > max_offset:
                    self.dropdown_offset = max_offset

            # Click chuột trái
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
                    self.paused = not self.paused  # bật/tắt pause
                elif self.show_dropdown:
                    start = self.dropdown_offset
                    end = min(start + self.dropdown_max_visible, len(self.algorithms))
                    for idx, i in enumerate(range(start, end)):
                        rect = pygame.Rect(self.dropdown.x, self.dropdown.y - (idx+1) * self.dropdown_item_height,  # vẽ lên trên
                            self.dropdown.width, self.dropdown_item_height)
                        if rect.collidepoint(e.pos):
                            self.select_algorithm(i)
                            break

    # Vẽ một bàn cờ
    def draw_board(self, board, x0, y0, title=""):
        # tiêu đề bàn cờ
        self.font.render_to(self.app.screen, (x0+30 , y0 - 30), title, (139, 69, 19), size=20)

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                # tạo các ô màu bàn cờ
                color = (240, 217, 181) if (i + j) % 2 == 0 else (181, 136, 99)
                rect = pygame.Rect(x0 + j * CELL, y0 + i * CELL, CELL, CELL)
                pygame.draw.rect(self.app.screen, color, rect)

                # viền nổi kiểu ridge
                pygame.draw.rect(self.app.screen, (200, 200, 200), rect, 2)  # viền sáng
                pygame.draw.rect(self.app.screen, (50, 50, 50), rect, 1)      # viền tối mảnh

                # vẽ quân ♜ nếu có
                if board[i][j] == 1:
                    char_surf, char_rect = self.font.render("♜", (0, 0, 0), size=40)
                    char_rect.center = rect.center
                    self.app.screen.blit(char_surf, char_rect)

    # Vẽ dropdown lên trên nút
    def draw_dropdown(self):
        if self.show_dropdown:
            start = self.dropdown_offset
            end = min(start + self.dropdown_max_visible, len(self.algorithms))
            for idx, i in enumerate(range(start, end)):
                rect = pygame.Rect(
                    self.dropdown.x,
                    self.dropdown.y - (idx+1) * self.dropdown_item_height,
                    self.dropdown.width,
                    self.dropdown_item_height
                )
                # nền
                pygame.draw.rect(self.app.screen, (240, 240, 240), rect, border_radius=5)
                pygame.draw.rect(self.app.screen, (0, 0, 0), rect, 1, border_radius=5)
                # chữ
                txt_surf, txt_rect = self.font.render(self.algorithms[i], (0, 0, 0), size=18)
                txt_rect.center = rect.center
                self.app.screen.blit(txt_surf, txt_rect)

    # Vẽ toàn bộ GameFrame
    def draw(self):
        # nền xanh lá nhẹ
        self.app.screen.fill((152, 251, 152))

        # vẽ 2 bàn cờ
        self.draw_board(self.left_board, *self.left_board_pos, "Left Board")
        # self.draw_board(self.right_board, *self.right_board_pos, "Right Board (GOAL)")

        # --- Nút Solve ---
        pygame.draw.rect(self.app.screen, (255, 255, 255), self.solve_button, border_radius=10)
        pygame.draw.rect(self.app.screen, (0, 0, 0), self.solve_button, 2, border_radius=10)
        txt_surf, txt_rect = self.font.render("Solve", (0, 0, 0), size=20)
        txt_rect.center = self.solve_button.center
        self.app.screen.blit(txt_surf, txt_rect)

        # --- Nút Back ---
        pygame.draw.rect(self.app.screen, (255, 255, 255), self.back_button, border_radius=10)
        pygame.draw.rect(self.app.screen, (0, 0, 0), self.back_button, 2, border_radius=10)
        txt_surf, txt_rect = self.font.render("Back", (0, 0, 0), size=20)
        txt_rect.center = self.back_button.center
        self.app.screen.blit(txt_surf, txt_rect)

        # --- Nút Pause/Resume ---
        pygame.draw.rect(self.app.screen, (255, 255, 255), self.pause_button, border_radius=10)
        pygame.draw.rect(self.app.screen, (0, 0, 0), self.pause_button, 2, border_radius=10)
        txt = "Resume" if self.paused else "Pause"
        txt_surf, txt_rect = self.font.render(txt, (0, 0, 0), size=20)
        txt_rect.center = self.pause_button.center
        self.app.screen.blit(txt_surf, txt_rect)

        # --- Nút Reset ---
        pygame.draw.rect(self.app.screen, (255, 255, 255), self.reset_button, border_radius=10)
        pygame.draw.rect(self.app.screen, (0, 0, 0), self.reset_button, 2, border_radius=10)
        txt_surf, txt_rect = self.font.render("Reset", (0, 0, 0), size=20)
        txt_rect.center = self.reset_button.center
        self.app.screen.blit(txt_surf, txt_rect)

        # --- Dropdown thuật toán ---
        pygame.draw.rect(self.app.screen, (211, 211, 211), self.dropdown, border_radius=10)  # nền nút
        pygame.draw.rect(self.app.screen, (0, 0, 0), self.dropdown, 2, border_radius=10)    # viền
        txt_surf, txt_rect = self.font.render("Choice Algorithm", (0, 0, 0), size=20)
        txt_rect.center = self.dropdown.center
        self.app.screen.blit(txt_surf, txt_rect)

        # Vẽ dropdown lên trên
        self.draw_dropdown()

        # --- Cập nhật animation ---
        self.update_animation()

    # Bắt đầu giải thuật toán
    def start_solver(self):
        self.reset_board()  # Chạy thuật toán được chọn
        self.run_classic_solver(self.selected_algo)

    def run_classic_solver(self, algo_name):
        # Các thuật toán BFS, DFS,...
        solvers = {
            "BFS": (RooksBFS, "bfs_pop_boards"),
            "DFS": (RooksDFS, "dfs_pop_boards"),
            "UCS": (RooksUCS, "ucs_pop_boards"),
            "DLS": (RooksDLS, "depth_limited_search"),
            "IDS": (RooksIDS, "ids_pop_boards"),
            "GS": (RooksGS, "gs_pop_boards"),
            "AS": (RooksAS, "as_pop_boards"),
            "Genetic": (RooksGenetic, "genetic_run"),
            "Hill": (RooksHillClimbing, "hill_pop_boards"),
            "simulatedAnnealing": (RooksSimulatedAnnealing, "simulatedAnnealing_pop_boards"),
            "beamSearch": (RooksBeamSearch, "beamSearch_pop_boards"),
            "AndOrSearch": (RooksAndOrSearch, "and_or_search"),
            "Belief": (RooksBelief, "belief_search"),
            "Backtracking": (RooksBacktracking, "backtracking"),
            "BTFC": (RooksBacktrackingForwardchecking, "backtracking"),
            "AC-3": (RooksBacktrackingAC3, "backtracking"),

        }
        if algo_name not in solvers:
            # Hiển thị message trên màn hình
            self.animating = False
            msg_surf, msg_rect = self.font.render(f"Algorithm {algo_name} not found!", (255, 0, 0), size=30)
            msg_rect.center = (self.app.screen.get_width() // 2, self.app.screen.get_height() // 2)
            self.app.screen.blit(msg_surf, msg_rect)
            pygame.display.flip()
            pygame.time.delay(200)  # hiện 2 giây
            return

        solver_class, method_name = solvers[algo_name] #lấy thuật toán đc chọn
        solver = solver_class() #tạo đối tượng thuật toán đc chọn

        result = getattr(solver, method_name)()  # chạy hàm thuật toán

        # Kiểm tra kết quả
        if result is None:
            self.animating = False
            msg_surf, msg_rect = self.font.render("No result", (255, 0, 0), size=30)
            msg_rect.center = (self.app.screen.get_width() // 2, self.app.screen.get_height() // 2)
            self.app.screen.blit(msg_surf, msg_rect)
            pygame.display.flip()
            pygame.time.delay(200)  # hiện 2 giây
            return

        # Nếu có kết quả
        self.animation_list = result
        self.animation_index = 0
        self.last_update = pygame.time.get_ticks()
        self.animating = True

    # update board các thuật toán
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
        """Reset left_board và dừng animation nếu có"""
        self.animating = False
        self.left_board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

    # Hàm xử lý các nút
    def click_solve(self):
        self.start_solver()

    def click_back(self):
        self.app.state = "MENU"
        self.app.game_frame = None

    def click_reset(self):
        # Dừng animation nếu đang chạy
        self.animating = False
        # Reset board
        self.left_board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

    def toggle_dropdown(self):
        self.show_dropdown = not self.show_dropdown

    def select_algorithm(self, algo_index):
        if 0 <= algo_index < len(self.algorithms):
            self.selected_algo = self.algorithms[algo_index]
            self.start_solver()  # chạy thuật toán ngay sau khi chọn
        self.show_dropdown = False
