import pygame
import pygame.freetype
from ui.GameFrame import GameFrame  # lớp game riêng

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1180, 510))
        pygame.display.set_caption("8 Rooks Game")
        self.clock = pygame.time.Clock()
        self.running = True

        # fonts
        self.font_big = pygame.freetype.SysFont("Times New Roman", 45, bold=True)
        self.font_small = pygame.freetype.SysFont("Times New Roman", 25, bold=True)

        # nút Start
        self.start_button = pygame.Rect(500, 300, 200, 60)

        # trạng thái
        self.state = "MENU"  # MENU

        # đối tượng GameFrame
        self.game_frame = None

    def handle_events(self):
        events = pygame.event.get()  # lấy 1 lần duy nhất

        if self.state == "MENU":
            # chỉ xử lý sự kiện khi đang ở menu
            for e in events:
                if e.type == pygame.QUIT:
                    self.running = False
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if self.start_button.collidepoint(pygame.mouse.get_pos()):
                        self.game_frame = GameFrame(self)
                        self.state = "PLAYING"

        elif self.state == "PLAYING":
            # không cần for ở đây, đưa hết cho GameFrame
            self.game_frame.handle_events(events)

    def update(self):
        pass

    def draw(self):
        if self.state == "MENU":
            # 1. tạo nền cho màn hình
            self.screen.fill((152, 251, 152))

            # 2. Thêm title vào screen
            text1 = "Welcome to 8x8 Rooks Game"
            self.font_big.render_to(self.screen, (320, 170), text1, (165, 42, 42))

            text2 = "Ready to play?"
            self.font_small.render_to(self.screen, (510, 230), text2, (165, 42, 42))

            # 3. Thêm nút start game
            pygame.draw.rect(self.screen, (255, 255, 255), self.start_button, border_radius=15)
            pygame.draw.rect(self.screen, (0, 0, 0), self.start_button, 2, border_radius=15)

            # Thêm title cho nút start
            text_surf, text_rect = self.font_small.render("Start!", (210, 42, 42))
            text_rect.center = self.start_button.center
            self.screen.blit(text_surf, text_rect)

        elif self.state == "PLAYING":
            # vẽ GameFrame
            self.game_frame.draw()


    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(200000)